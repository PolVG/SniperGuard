import os
import shutil
import subprocess
import sqlite3
from pathlib import Path
import winreg


# =========================================================
# UTILITATS
# =========================================================

def taskkill(image_name: str):
    """Tanca un procés per nom (ex: chrome.exe). No peta si no existeix."""
    try:
        subprocess.run(
            ["taskkill", "/IM", image_name, "/F"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception:
        pass


def borrar_contenido_carpeta(ruta: Path):
    """Borra TOT el contingut d'una carpeta, però NO elimina la carpeta en sí."""
    if not ruta.exists():
        return
    if not ruta.is_dir():
        return

    print(f"[INFO] Buident carpeta (contingut): {ruta}")
    for item in ruta.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
                print(f"  [OK] Fitxer esborrat: {item.name}")
            elif item.is_dir():
                shutil.rmtree(item)
                print(f"  [OK] Carpeta esborrada: {item.name}")
        except Exception as e:
            print(f"  [WARN] No s'ha pogut esborrar: {item.name} -> {e}")


def borrar_archivo(path: Path, label: str):
    """Esborra un fitxer si existeix."""
    if path.exists() and path.is_file():
        try:
            path.unlink()
            print(f"  [OK] {label}: esborrat ({path.name})")
        except Exception as e:
            print(f"  [WARN] {label}: no s'ha pogut esborrar ({path.name}) -> {e}")


def borrar_archivos_por_patron(dirpath: Path, patterns: list[str], label: str):
    """Esborra fitxers dins dirpath que compleixin patterns (glob)."""
    if not dirpath.exists() or not dirpath.is_dir():
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
        pass
    return out


def detect_installed_browsers_registry():
    found = []
    for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        for p in REG_PATHS:
            found.extend(enum_subkeys(root, p))

    unique, seen = [], set()
    for x in found:
        if x not in seen:
            unique.append(x)
            seen.add(x)
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
    return normalized


# =========================================================
# PERFILS CHROMIUM
# =========================================================

def chromium_profiles(base_user_data: Path):
    if not base_user_data.exists():
        return []
    profiles = []
    for d in base_user_data.iterdir():
        if d.is_dir() and (d.name == "Default" or d.name.startswith("Profile ")):
            profiles.append(d)
    return profiles


def clean_chromium_all(vendor: str, product: str, process_name: str):
    """
    Chromium (Chrome/Edge/Brave/Opera):
      - Cache: Cache, Code Cache, GPUCache, Media Cache, Service Worker CacheStorage
      - Cookies: Cookies + Network\Cookies (+ journals)
      - History: History (+ journals)
    """
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        print("[WARN] LOCALAPPDATA no definit; no es pot netejar Chromium.")
        return

    base = Path(local_appdata) / vendor / product / "User Data"
    if not base.exists():
        print(f"[SKIP] No trobat perfil: {base}")
        return

    print(f"\n===== NETEJA COMPLETA {vendor} {product} (cache + cookies + historial) =====")
    print(f"[INFO] Tancant {process_name}…")
    taskkill(process_name)

    profiles = chromium_profiles(base)
    if not profiles:
        print("[WARN] No s'han trobat perfils (Default/Profile X).")
        return

    for prof in profiles:
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


# =========================================================
# FIREFOX: cache + cookies + historial (sense bookmarks)
# =========================================================

def firefox_clear_history_preserve_bookmarks(places_db: Path):
    """
    Esborra historial de Firefox dins places.sqlite mantenint bookmarks.
    Estratègia:
      - Esborra visites
      - Esborra input history
      - Reseteja visit_count/last_visit_date només per URL no bookmarkades
    """
    if not places_db.exists():
        return

    try:
        conn = sqlite3.connect(str(places_db))
        cur = conn.cursor()

        cur.execute("PRAGMA foreign_keys=OFF;")

        # Esborrar visites
        cur.execute("DELETE FROM moz_historyvisits;")

        # Esborrar historial d'inputs (barra adreces)
        cur.execute("DELETE FROM moz_inputhistory;")

        # Resetejar comptadors per pàgines NO bookmarkades
        cur.execute("""
            UPDATE moz_places
            SET visit_count = 0,
                last_visit_date = NULL,
                hidden = 1
            WHERE id NOT IN (
                SELECT fk FROM moz_bookmarks WHERE fk IS NOT NULL
            );
        """)

        # Neteja extra (opcional): taules de metadades temporals
        # (si no existeixen en alguna versió, ignorem)
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
        print("  [OK] Historial Firefox netejat (bookmarks preservats).")

    except Exception as e:
        print(f"  [WARN] No s'ha pogut netejar historial Firefox (places.sqlite) -> {e}")


def clean_firefox_all():
    """
    Firefox:
      - Cache: cache2 (contingut)
      - Cookies: cookies.sqlite
      - Historial: places.sqlite (neteja interna per preservar bookmarks)
    """
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        print("[WARN] LOCALAPPDATA no definit; no es pot netejar Firefox.")
        return

    profiles_root = Path(local_appdata) / "Mozilla" / "Firefox" / "Profiles"
    if not profiles_root.exists():
        print(f"[SKIP] No trobat: {profiles_root}")
        return

    print("\n===== NETEJA COMPLETA FIREFOX (cache + cookies + historial) =====")
    print("[INFO] Tancant firefox.exe…")
    taskkill("firefox.exe")

    for prof in profiles_root.iterdir():
        if not prof.is_dir():
            continue

        print(f"\n[INFO] Perfil: {prof.name}")

        # 1) CACHE
        borrar_contenido_carpeta(prof / "cache2")

        # 2) COOKIES
        borrar_archivo(prof / "cookies.sqlite", "Cookies Firefox")
        borrar_archivo(prof / "cookies.sqlite-wal", "Cookies Firefox")
        borrar_archivo(prof / "cookies.sqlite-shm", "Cookies Firefox")

        # 3) HISTORIAL (preservant bookmarks)
        firefox_clear_history_preserve_bookmarks(prof / "places.sqlite")


# =========================================================
# MAIN
# =========================================================

def main():
    print("===== DETECCIÓ NAVEGADORS (REGISTRE) =====")
    reg_browsers = detect_installed_browsers_registry()

    if reg_browsers:
        for b in reg_browsers:
            print(" -", b)
    else:
        print("Cap navegador detectat segons el registre oficial.")

    detected = normalize_browsers(reg_browsers)
    print("\n===== NAVEGADORS NORMALITZATS =====")
    if detected:
        print("Detectats:", ", ".join(sorted(detected)))
    else:
        print("No s'ha pogut mapar cap navegador conegut (Chrome/Edge/Firefox/Brave/Opera).")

    # Chromium family
    if "chrome" in detected:
        clean_chromium_all("Google", "Chrome", "chrome.exe")
    else:
        print("\n[SKIP] Chrome no detectat.")

    if "edge" in detected:
        clean_chromium_all("Microsoft", "Edge", "msedge.exe")
    else:
        print("\n[SKIP] Edge no detectat.")

    if "brave" in detected:
        clean_chromium_all("BraveSoftware", "Brave-Browser", "brave.exe")
    else:
        print("\n[SKIP] Brave no detectat.")

    # Firefox
    if "firefox" in detected:
        clean_firefox_all()
    else:
        print("\n[SKIP] Firefox no detectat.")

    # Opera (paths poden variar segons Stable/GX; provem ambdós)
    if "opera" in detected:
        clean_chromium_all("Opera Software", "Opera Stable", "opera.exe")
        clean_chromium_all("Opera Software", "Opera GX Stable", "opera.exe")
    else:
        print("\n[SKIP] Opera no detectat.")

    print("\n===== PROCÉS FINALITZAT =====")


if __name__ == "__main__":
    main()
