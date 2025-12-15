import os
import shutil
import subprocess
import sqlite3
from pathlib import Path
import winreg

from modules.LogRegister import log


# =========================================================
# UTILITATS
# =========================================================

def taskkill(image_name: str):
    """Tanca un procés per nom (ex: chrome.exe). No peta si no existeix."""
    log(f"Intentant tancar procés: {image_name}", 100)
    try:
        res = subprocess.run(
            ["taskkill", "/IM", image_name, "/F"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if res.returncode == 0:
            log(f"taskkill OK: {image_name}", 200)
        else:
            # Sovint és “not found”; ho tractem com a warning
            err = (res.stderr or "").strip()
            out = (res.stdout or "").strip()
            log(f"taskkill returncode={res.returncode} | proc={image_name} | stdout='{out}' | stderr='{err}'", 300)

    except Exception as e:
        log(f"taskkill excepció: proc={image_name} ({repr(e)})", 400)


def borrar_contenido_carpeta(ruta: Path):
    """Borra TOT el contingut d'una carpeta, però NO elimina la carpeta en sí."""
    if not ruta.exists():
        log(f"[SKIP] Carpeta no existeix (no es buida): {ruta}", 100)
        return
    if not ruta.is_dir():
        log(f"[SKIP] Ruta no és carpeta (no es buida): {ruta}", 100)
        return

    log(f"Inici buidat contingut carpeta: {ruta}", 200)
    print(f"[INFO] Buident carpeta (contingut): {ruta}")

    for item in ruta.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
                log(f"[OK] Fitxer esborrat: {item}", 250)
                print(f"  [OK] Fitxer esborrat: {item.name}")
            elif item.is_dir():
                shutil.rmtree(item)
                log(f"[OK] Carpeta esborrada: {item}", 250)
                print(f"  [OK] Carpeta esborrada: {item.name}")
        except Exception as e:
            log(f"[WARN] No s'ha pogut esborrar: {item} ({repr(e)})", 300)
            print(f"  [WARN] No s'ha pogut esborrar: {item.name} -> {e}")

    log(f"Fi buidat carpeta: {ruta}", 200)


def borrar_archivo(path: Path, label: str):
    """Esborra un fitxer si existeix."""
    if path.exists() and path.is_file():
        try:
            path.unlink()
            log(f"[OK] {label}: esborrat ({path})", 250)
            print(f"  [OK] {label}: esborrat ({path.name})")
        except Exception as e:
            log(f"[WARN] {label}: no s'ha pogut esborrar ({path}) ({repr(e)})", 300)
            print(f"  [WARN] {label}: no s'ha pogut esborrar ({path.name}) -> {e}")
    else:
        log(f"[SKIP] {label}: no existeix ({path})", 100)


def borrar_archivos_por_patron(dirpath: Path, patterns: list[str], label: str):
    """Esborra fitxers dins dirpath que compleixin patterns (glob)."""
    if not dirpath.exists() or not dirpath.is_dir():
        log(f"[SKIP] Dir no existeix per patrons ({label}): {dirpath}", 100)
        return
    for pat in patterns:
        for p in dirpath.glob(pat):
            borrar_archivo(p, label)


# =========================================================
# DETECCIÓ NAVEGADORS VIA REGISTRE (StartMenuInternet)
# =========================================================

REG_PATHS = [
    r"Software\Clients\StartMenuInternet",
    r"Software\WOW6432Node\Clients\StartMenuInternet",
]


def enum_subkeys(root, path):
    out = []
    try:
        key = winreg.OpenKey(root, path)
        i = 0
        while True:
            try:
                out.append(winreg.EnumKey(key, i))
                i += 1
            except OSError:
                break
        winreg.CloseKey(key)
    except FileNotFoundError:
        # normal
        log(f"Clau registre inexistent: root={root} path={path}", 100)
    except Exception as e:
        log(f"Error enum_subkeys: root={root} path={path} ({repr(e)})", 400)
    return out


def detect_installed_browsers_registry():
    log("Inici detecció navegadors via registre", 200)

    found = []
    for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        for p in REG_PATHS:
            sub = enum_subkeys(root, p)
            if sub:
                log(f"Registre: root={root} path={p} -> {len(sub)} entrades", 100)
            found.extend(sub)

    unique, seen = [], set()
    for x in found:
        if x not in seen:
            unique.append(x)
            seen.add(x)

    log(f"Fi detecció registre: {len(unique)} entrades úniques", 250)
    return unique


def normalize_browsers(reg_names):
    normalized = set()
    for name in reg_names:
        low = name.lower()
        if "chrome" in low:
            normalized.add("chrome")
        elif "edge" in low or "msedge" in low:
            normalized.add("edge")
        elif "firefox" in low or "mozilla" in low:
            normalized.add("firefox")
        elif "brave" in low:
            normalized.add("brave")
        elif "opera" in low:
            normalized.add("opera")

    log(f"Navegadors normalitzats: {', '.join(sorted(normalized)) if normalized else '(cap)'}", 250)
    return normalized


# =========================================================
# PERFILS CHROMIUM
# =========================================================

def chromium_profiles(base_user_data: Path):
    if not base_user_data.exists():
        log(f"[SKIP] Chromium base no existeix: {base_user_data}", 100)
        return []
    profiles = []
    try:
        for d in base_user_data.iterdir():
            if d.is_dir() and (d.name == "Default" or d.name.startswith("Profile ")):
                profiles.append(d)
    except Exception as e:
        log(f"Error enumerant perfils Chromium: {base_user_data} ({repr(e)})", 400)
    log(f"Perfils Chromium trobats: base={base_user_data} count={len(profiles)}", 200)
    return profiles


def clean_chromium_all(vendor: str, product: str, process_name: str):
    """
    Chromium (Chrome/Edge/Brave/Opera):
      - Cache: Cache, Code Cache, GPUCache, Media Cache, Service Worker CacheStorage
      - Cookies: Cookies + Network\Cookies (+ journals)
      - History: History (+ journals)
    """
    log(f"Inici neteja Chromium: {vendor} {product} | process={process_name}", 200)

    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        log("LOCALAPPDATA no definit; no es pot netejar Chromium.", 400)
        print("[WARN] LOCALAPPDATA no definit; no es pot netejar Chromium.")
        return

    base = Path(local_appdata) / vendor / product / "User Data"
    log(f"Ruta base Chromium: {base}", 100)

    if not base.exists():
        log(f"[SKIP] No trobat perfil Chromium: {base}", 250)
        print(f"[SKIP] No trobat perfil: {base}")
        return

    print(f"\n===== NETEJA COMPLETA {vendor} {product} (cache + cookies + historial) =====")
    print(f"[INFO] Tancant {process_name}…")
    taskkill(process_name)

    profiles = chromium_profiles(base)
    if not profiles:
        log(f"[WARN] No s'han trobat perfils Chromium (Default/Profile X) a {base}", 300)
        print("[WARN] No s'han trobat perfils (Default/Profile X).")
        return

    for prof in profiles:
        log(f"Netejant perfil Chromium: {vendor} {product} | perfil={prof.name}", 200)
        print(f"\n[INFO] Perfil: {prof.name}")

        # 1) CACHE
        cache_dirs = [
            prof / "Cache",
            prof / "Code Cache",
            prof / "GPUCache",
            prof / "Media Cache",
            prof / "Service Worker" / "CacheStorage",
        ]
        for c in cache_dirs:
            borrar_contenido_carpeta(c)

        # 2) COOKIES (Chromium)
        borrar_archivo(prof / "Cookies", "Cookies")
        borrar_archivo(prof / "Cookies-journal", "Cookies")
        net_dir = prof / "Network"
        borrar_archivo(net_dir / "Cookies", "Cookies (Network)")
        borrar_archivo(net_dir / "Cookies-journal", "Cookies (Network)")

        # 3) HISTORIAL
        borrar_archivo(prof / "History", "Historial")
        borrar_archivo(prof / "History-journal", "Historial")
        borrar_archivo(prof / "Visited Links", "Visited Links")
        borrar_archivo(prof / "Visited Links-journal", "Visited Links")

    log(f"Fi neteja Chromium: {vendor} {product}", 200)


# =========================================================
# FIREFOX: cache + cookies + historial (sense bookmarks)
# =========================================================

def firefox_clear_history_preserve_bookmarks(places_db: Path):
    """
    Esborra historial de Firefox dins places.sqlite mantenint bookmarks.
    """
    if not places_db.exists():
        log(f"[SKIP] places.sqlite no existeix: {places_db}", 100)
        return

    log(f"Inici neteja historial Firefox preservant bookmarks: {places_db}", 200)

    try:
        conn = sqlite3.connect(str(places_db))
        cur = conn.cursor()

        cur.execute("PRAGMA foreign_keys=OFF;")

        cur.execute("DELETE FROM moz_historyvisits;")
        cur.execute("DELETE FROM moz_inputhistory;")

        cur.execute("""
            UPDATE moz_places
            SET visit_count = 0,
                last_visit_date = NULL,
                hidden = 1
            WHERE id NOT IN (
                SELECT fk FROM moz_bookmarks WHERE fk IS NOT NULL
            );
        """)

        # Opcional: ignorem si no existeixen
        try:
            cur.execute("DELETE FROM moz_annos;")
        except Exception:
            pass
        try:
            cur.execute("DELETE FROM moz_items_annos;")
        except Exception:
            pass

        conn.commit()
        conn.close()

        log("Historial Firefox netejat correctament (bookmarks preservats)", 250)
        print("  [OK] Historial Firefox netejat (bookmarks preservats).")

    except Exception as e:
        log(f"No s'ha pogut netejar historial Firefox (places.sqlite): {places_db} ({repr(e)})", 400)
        print(f"  [WARN] No s'ha pogut netejar historial Firefox (places.sqlite) -> {e}")


def clean_firefox_all():
    """
    Firefox:
      - Cache: cache2 (contingut)
      - Cookies: cookies.sqlite
      - Historial: places.sqlite (neteja interna per preservar bookmarks)
    """
    log("Inici neteja Firefox (cache + cookies + historial)", 200)

    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        log("LOCALAPPDATA no definit; no es pot netejar Firefox.", 400)
        print("[WARN] LOCALAPPDATA no definit; no es pot netejar Firefox.")
        return

    profiles_root = Path(local_appdata) / "Mozilla" / "Firefox" / "Profiles"
    log(f"Ruta perfils Firefox: {profiles_root}", 100)

    if not profiles_root.exists():
        log(f"[SKIP] No trobat Firefox profiles root: {profiles_root}", 250)
        print(f"[SKIP] No trobat: {profiles_root}")
        return

    print("\n===== NETEJA COMPLETA FIREFOX (cache + cookies + historial) =====")
    print("[INFO] Tancant firefox.exe…")
    taskkill("firefox.exe")

    for prof in profiles_root.iterdir():
        if not prof.is_dir():
            continue

        log(f"Netejant perfil Firefox: {prof.name}", 200)
        print(f"\n[INFO] Perfil: {prof.name}")

        borrar_contenido_carpeta(prof / "cache2")

        borrar_archivo(prof / "cookies.sqlite", "Cookies Firefox")
        borrar_archivo(prof / "cookies.sqlite-wal", "Cookies Firefox")
        borrar_archivo(prof / "cookies.sqlite-shm", "Cookies Firefox")

        firefox_clear_history_preserve_bookmarks(prof / "places.sqlite")

    log("Fi neteja Firefox", 200)


# =========================================================
# MAIN
# =========================================================

def main():
    log("==== Inici neteja navegadors (DEL) ====", 200)

    print("===== DETECCIÓ NAVEGADORS (REGISTRE) =====")
    reg_browsers = detect_installed_browsers_registry()

    if reg_browsers:
        for b in reg_browsers:
            print(" -", b)
        log(f"Navegadors detectats (raw): {', '.join(reg_browsers)}", 200)
    else:
        print("Cap navegador detectat segons el registre oficial.")
        log("Cap navegador detectat segons el registre oficial (raw)", 300)

    detected = normalize_browsers(reg_browsers)
    print("\n===== NAVEGADORS NORMALITZATS =====")
    if detected:
        print("Detectats:", ", ".join(sorted(detected)))
    else:
        print("No s'ha pogut mapar cap navegador conegut (Chrome/Edge/Firefox/Brave/Opera).")
        log("No s'ha pogut mapar cap navegador conegut", 300)

    if "chrome" in detected:
        clean_chromium_all("Google", "Chrome", "chrome.exe")
    else:
        log("[SKIP] Chrome no detectat", 250)
        print("\n[SKIP] Chrome no detectat.")

    if "edge" in detected:
        clean_chromium_all("Microsoft", "Edge", "msedge.exe")
    else:
        log("[SKIP] Edge no detectat", 250)
        print("\n[SKIP] Edge no detectat.")

    if "brave" in detected:
        clean_chromium_all("BraveSoftware", "Brave-Browser", "brave.exe")
    else:
        log("[SKIP] Brave no detectat", 250)
        print("\n[SKIP] Brave no detectat.")

    if "firefox" in detected:
        clean_firefox_all()
    else:
        log("[SKIP] Firefox no detectat", 250)
        print("\n[SKIP] Firefox no detectat.")

    if "opera" in detected:
        clean_chromium_all("Opera Software", "Opera Stable", "opera.exe")
        clean_chromium_all("Opera Software", "Opera GX Stable", "opera.exe")
    else:
        log("[SKIP] Opera no detectat", 250)
        print("\n[SKIP] Opera no detectat.")

    print("\n===== PROCÉS FINALITZAT =====")
    log("==== Fi neteja navegadors (DEL) ====", 200)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"Excepció no controlada a __main__: {repr(e)}", 600)
        raise
