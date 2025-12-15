import os
from pathlib import Path
import winreg

from modules.LogRegister import log

# =========================================================
# CONFIG BARÒMETRE (MB)
# =========================================================
URGENT_TOTAL_MB = 1024      # 🔴 si total (cache+cookies+hist) >= 1GB
RECOMM_TOTAL_MB = 250       # 🟡 si total >= 250MB

URGENT_PART_MB = 512        # 🔴 si una part (ex: cache) >= 512MB
RECOMM_PART_MB = 100        # 🟡 si una part >= 100MB


# =========================================================
# UTILITATS MIDA
# =========================================================
def bytes_to_mb(b: int) -> float:
    return round(b / (1024 * 1024), 2)

def file_size_bytes(p: Path) -> int:
    try:
        if p.exists() and p.is_file():
            return p.stat().st_size
        return 0
    except Exception as e:
        log(f"No s'ha pogut llegir mida fitxer: {p} ({repr(e)})", 300)
        return 0

def dir_size_bytes(p: Path) -> int:
    if not p.exists() or not p.is_dir():
        return 0

    total = 0
    try:
        for root, dirs, files in os.walk(p):
            for f in files:
                fp = Path(root) / f
                try:
                    total += fp.stat().st_size
                except Exception as e:
                    # Error puntual: no aturem execució
                    log(f"No s'ha pogut accedir a fitxer dins dir_size_bytes: {fp} ({repr(e)})", 300)
                    continue
    except Exception as e:
        log(f"Error recorrent directori: {p} ({repr(e)})", 400)

    return total

def barometre(mb: float, urgent_mb: float, recomm_mb: float):
    if mb >= urgent_mb:
        return "🔴", "URGENT"
    if mb >= recomm_mb:
        return "🟡", "RECOMANABLE"
    return "🟢", "NO CAL (però no fa mal)"


# =========================================================
# DETECCIÓ NAVEGADORS VIA REGISTRE
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
        # Normal (no totes les màquines tenen totes les rutes)
        log(f"Clau registre inexistent: root={root} path={path}", 100)
    except Exception as e:
        log(f"Error llegint registre: root={root} path={path} ({repr(e)})", 400)
    return out

def detect_installed_browsers_registry():
    log("Inici detecció de navegadors via registre (StartMenuInternet)", 200)

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

    log(f"Detecció registre finalitzada: {len(unique)} navegadors (raw)", 250)
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
        log(f"Chromium base no existeix: {base_user_data}", 100)
        return []

    profiles = []
    try:
        for d in base_user_data.iterdir():
            if d.is_dir() and (d.name == "Default" or d.name.startswith("Profile ")):
                profiles.append(d)
    except Exception as e:
        log(f"Error enumerant perfils Chromium: {base_user_data} ({repr(e)})", 400)

    log(f"Perfils Chromium trobats a {base_user_data}: {len(profiles)}", 200)
    return profiles

def chromium_profile_sizes(profile_dir: Path):
    # CACHE (sumem diverses carpetes)
    cache_dirs = [
        profile_dir / "Cache",
        profile_dir / "Code Cache",
        profile_dir / "GPUCache",
        profile_dir / "Media Cache",
        profile_dir / "Service Worker" / "CacheStorage",
    ]
    cache_bytes = sum(dir_size_bytes(p) for p in cache_dirs)

    # COOKIES (2 ubicacions possibles)
    cookies_bytes = 0
    cookies_bytes += file_size_bytes(profile_dir / "Cookies")
    cookies_bytes += file_size_bytes(profile_dir / "Cookies-journal")
    net = profile_dir / "Network"
    cookies_bytes += file_size_bytes(net / "Cookies")
    cookies_bytes += file_size_bytes(net / "Cookies-journal")

    # HISTORIAL
    hist_bytes = 0
    hist_bytes += file_size_bytes(profile_dir / "History")
    hist_bytes += file_size_bytes(profile_dir / "History-journal")
    hist_bytes += file_size_bytes(profile_dir / "Visited Links")
    hist_bytes += file_size_bytes(profile_dir / "Visited Links-journal")

    return cache_bytes, cookies_bytes, hist_bytes

def report_chromium(vendor: str, product: str):
    log(f"Inici report Chromium: vendor={vendor} product={product}", 200)

    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        log("LOCALAPPDATA no definit; no es pot analitzar Chromium.", 400)
        print("[WARN] LOCALAPPDATA no definit; no es pot analitzar Chromium.")
        return

    base = Path(local_appdata) / vendor / product / "User Data"
    log(f"Ruta base Chromium: {base}", 100)

    if not base.exists():
        log(f"[SKIP] Chromium no trobat: {vendor} {product} ({base})", 250)
        print(f"[SKIP] {vendor} {product}: no trobat ({base})")
        return

    print(f"\n===== BARÒMETRE {vendor} {product} =====")
    profiles = chromium_profiles(base)
    if not profiles:
        log(f"No s'han trobat perfils Chromium a {base}", 300)
        print("[WARN] No s'han trobat perfils (Default/Profile X).")
        return

    total_all = 0.0

    for prof in profiles:
        log(f"Analitzant perfil Chromium: {vendor}/{product} perfil={prof.name}", 100)

        cache_b, cookies_b, hist_b = chromium_profile_sizes(prof)
        cache_mb = bytes_to_mb(cache_b)
        cookies_mb = bytes_to_mb(cookies_b)
        hist_mb = bytes_to_mb(hist_b)
        total_mb = round(cache_mb + cookies_mb + hist_mb, 2)
        total_all += total_mb

        c_col, c_txt = barometre(cache_mb, URGENT_PART_MB, RECOMM_PART_MB)
        k_col, k_txt = barometre(cookies_mb, URGENT_PART_MB, RECOMM_PART_MB)
        h_col, h_txt = barometre(hist_mb, URGENT_PART_MB, RECOMM_PART_MB)
        t_col, t_txt = barometre(total_mb, URGENT_TOTAL_MB, RECOMM_TOTAL_MB)

        # Logs clau per auditoria
        log(
            f"[{vendor} {product} | {prof.name}] cache={cache_mb}MB({c_col}) "
            f"cookies={cookies_mb}MB({k_col}) hist={hist_mb}MB({h_col}) total={total_mb}MB({t_col})",
            250
        )

        print(f"\n[Perfil: {prof.name}]")
        print(f"  Cache    : {cache_mb} MB   -> {c_col} {c_txt}")
        print(f"  Cookies  : {cookies_mb} MB -> {k_col} {k_txt}")
        print(f"  Historial: {hist_mb} MB    -> {h_col} {h_txt}")
        print(f"  TOTAL    : {total_mb} MB   -> {t_col} {t_txt}")

    tcol, ttxt = barometre(total_all, URGENT_TOTAL_MB, RECOMM_TOTAL_MB)
    log(f"[RESUM {vendor} {product}] total perfils={round(total_all, 2)}MB estat={tcol} {ttxt}", 250)
    print(f"\n[RESUM {vendor} {product}] Total perfils: {round(total_all, 2)} MB -> {tcol} {ttxt}")

    log(f"Fi report Chromium: vendor={vendor} product={product}", 200)


# =========================================================
# FIREFOX
# =========================================================
def firefox_profile_sizes(profile_dir: Path):
    # CACHE
    cache_b = dir_size_bytes(profile_dir / "cache2")

    # COOKIES
    cookies_b = 0
    cookies_b += file_size_bytes(profile_dir / "cookies.sqlite")
    cookies_b += file_size_bytes(profile_dir / "cookies.sqlite-wal")
    cookies_b += file_size_bytes(profile_dir / "cookies.sqlite-shm")

    # HISTORIAL
    hist_b = 0
    hist_b += file_size_bytes(profile_dir / "places.sqlite")
    hist_b += file_size_bytes(profile_dir / "places.sqlite-wal")
    hist_b += file_size_bytes(profile_dir / "places.sqlite-shm")

    return cache_b, cookies_b, hist_b

def report_firefox():
    log("Inici report Firefox", 200)

    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        log("LOCALAPPDATA no definit; no es pot analitzar Firefox.", 400)
        print("[WARN] LOCALAPPDATA no definit; no es pot analitzar Firefox.")
        return

    profiles_root = Path(local_appdata) / "Mozilla" / "Firefox" / "Profiles"
    log(f"Ruta perfils Firefox: {profiles_root}", 100)

    if not profiles_root.exists():
        log(f"[SKIP] Firefox no trobat ({profiles_root})", 250)
        print(f"[SKIP] Firefox: no trobat ({profiles_root})")
        return

    print("\n===== BARÒMETRE FIREFOX =====")
    total_all = 0.0

    for prof in profiles_root.iterdir():
        if not prof.is_dir():
            continue

        log(f"Analitzant perfil Firefox: {prof.name}", 100)

        cache_b, cookies_b, hist_b = firefox_profile_sizes(prof)
        cache_mb = bytes_to_mb(cache_b)
        cookies_mb = bytes_to_mb(cookies_b)
        hist_mb = bytes_to_mb(hist_b)
        total_mb = round(cache_mb + cookies_mb + hist_mb, 2)
        total_all += total_mb

        c_col, c_txt = barometre(cache_mb, URGENT_PART_MB, RECOMM_PART_MB)
        k_col, k_txt = barometre(cookies_mb, URGENT_PART_MB, RECOMM_PART_MB)
        h_col, h_txt = barometre(hist_mb, URGENT_PART_MB, RECOMM_PART_MB)
        t_col, t_txt = barometre(total_mb, URGENT_TOTAL_MB, RECOMM_TOTAL_MB)

        log(
            f"[Firefox | {prof.name}] cache={cache_mb}MB({c_col}) "
            f"cookies={cookies_mb}MB({k_col}) hist={hist_mb}MB({h_col}) total={total_mb}MB({t_col})",
            250
        )

        print(f"\n[Perfil: {prof.name}]")
        print(f"  Cache    : {cache_mb} MB   -> {c_col} {c_txt}")
        print(f"  Cookies  : {cookies_mb} MB -> {k_col} {k_txt}")
        print(f"  Historial: {hist_mb} MB    -> {h_col} {h_txt}")
        print("             (Nota: a Firefox això és places.sqlite; inclou també marcadors/bookmarks.)")
        print(f"  TOTAL    : {total_mb} MB   -> {t_col} {t_txt}")

    tcol, ttxt = barometre(total_all, URGENT_TOTAL_MB, RECOMM_TOTAL_MB)
    log(f"[RESUM FIREFOX] total perfils={round(total_all, 2)}MB estat={tcol} {ttxt}", 250)
    print(f"\n[RESUM FIREFOX] Total perfils: {round(total_all, 2)} MB -> {tcol} {ttxt}")

    log("Fi report Firefox", 200)


# =========================================================
# MAIN
# =========================================================
def main():
    log("==== Inici diagnòstic navegadors (BAR) ====", 200)

    print("===== DETECCIÓ NAVEGADORS (REGISTRE) =====")
    reg_browsers = detect_installed_browsers_registry()

    if reg_browsers:
        for b in reg_browsers:
            print(" -", b)
        log(f"Navegadors detectats (raw): {', '.join(reg_browsers)}", 200)
    else:
        print("Cap navegador detectat segons el registre oficial.")
        log("Cap navegador detectat segons el registre (raw)", 300)

    detected = normalize_browsers(reg_browsers)

    print("\n===== NAVEGADORS NORMALITZATS =====")
    if detected:
        print("Detectats:", ", ".join(sorted(detected)))
    else:
        print("No s'ha pogut mapar cap navegador conegut (Chrome/Edge/Firefox/Brave/Opera).")
        log("No s'ha pogut normalitzar cap navegador conegut", 300)

    # Chromium family
    if "chrome" in detected:
        report_chromium("Google", "Chrome")
    else:
        log("[SKIP] Chrome no detectat", 250)
        print("\n[SKIP] Chrome no detectat.")

    if "edge" in detected:
        report_chromium("Microsoft", "Edge")
    else:
        log("[SKIP] Edge no detectat", 250)
        print("\n[SKIP] Edge no detectat.")

    if "brave" in detected:
        report_chromium("BraveSoftware", "Brave-Browser")
    else:
        log("[SKIP] Brave no detectat", 250)
        print("\n[SKIP] Brave no detectat.")

    if "opera" in detected:
        report_chromium("Opera Software", "Opera Stable")
        report_chromium("Opera Software", "Opera GX Stable")
    else:
        log("[SKIP] Opera no detectat", 250)
        print("\n[SKIP] Opera no detectat.")

    # Firefox
    if "firefox" in detected:
        report_firefox()
    else:
        log("[SKIP] Firefox no detectat", 250)
        print("\n[SKIP] Firefox no detectat.")

    print("\n===== DIAGNÒSTIC FINALITZAT (NO S'HA ESBORRAT RES) =====")
    log("==== Fi diagnòstic navegadors (BAR) ====", 200)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"Excepció no controlada a __main__: {repr(e)}", 600)
        raise
