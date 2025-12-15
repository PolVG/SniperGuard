import os
from pathlib import Path
import winreg

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
        return p.stat().st_size if p.exists() and p.is_file() else 0
    except Exception:
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
                except Exception:
                    pass
    except Exception:
        pass
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
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        print("[WARN] LOCALAPPDATA no definit; no es pot analitzar Chromium.")
        return

    base = Path(local_appdata) / vendor / product / "User Data"
    if not base.exists():
        print(f"[SKIP] {vendor} {product}: no trobat ({base})")
        return

    print(f"\n===== BARÒMETRE {vendor} {product} =====")
    profiles = chromium_profiles(base)
    if not profiles:
        print("[WARN] No s'han trobat perfils (Default/Profile X).")
        return

    total_all = 0.0

    for prof in profiles:
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

        print(f"\n[Perfil: {prof.name}]")
        print(f"  Cache    : {cache_mb} MB   -> {c_col} {c_txt}")
        print(f"  Cookies  : {cookies_mb} MB -> {k_col} {k_txt}")
        print(f"  Historial: {hist_mb} MB    -> {h_col} {h_txt}")
        print(f"  TOTAL    : {total_mb} MB   -> {t_col} {t_txt}")

    tcol, ttxt = barometre(total_all, URGENT_TOTAL_MB, RECOMM_TOTAL_MB)
    print(f"\n[RESUM {vendor} {product}] Total perfils: {round(total_all, 2)} MB -> {tcol} {ttxt}")


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

    # HISTORIAL (i bookmarks van a places.sqlite; el pes serveix igual per decidir)
    hist_b = 0
    hist_b += file_size_bytes(profile_dir / "places.sqlite")
    hist_b += file_size_bytes(profile_dir / "places.sqlite-wal")
    hist_b += file_size_bytes(profile_dir / "places.sqlite-shm")

    return cache_b, cookies_b, hist_b

def report_firefox():
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        print("[WARN] LOCALAPPDATA no definit; no es pot analitzar Firefox.")
        return

    profiles_root = Path(local_appdata) / "Mozilla" / "Firefox" / "Profiles"
    if not profiles_root.exists():
        print(f"[SKIP] Firefox: no trobat ({profiles_root})")
        return

    print("\n===== BARÒMETRE FIREFOX =====")
    total_all = 0.0

    for prof in profiles_root.iterdir():
        if not prof.is_dir():
            continue

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

        print(f"\n[Perfil: {prof.name}]")
        print(f"  Cache    : {cache_mb} MB   -> {c_col} {c_txt}")
        print(f"  Cookies  : {cookies_mb} MB -> {k_col} {k_txt}")
        print(f"  Historial: {hist_mb} MB    -> {h_col} {h_txt}")
        print("             (Nota: a Firefox això és places.sqlite; inclou també marcadors/bookmarks.)")
        print(f"  TOTAL    : {total_mb} MB   -> {t_col} {t_txt}")

    tcol, ttxt = barometre(total_all, URGENT_TOTAL_MB, RECOMM_TOTAL_MB)
    print(f"\n[RESUM FIREFOX] Total perfils: {round(total_all, 2)} MB -> {tcol} {ttxt}")


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
        report_chromium("Google", "Chrome")
    else:
        print("\n[SKIP] Chrome no detectat.")

    if "edge" in detected:
        report_chromium("Microsoft", "Edge")
    else:
        print("\n[SKIP] Edge no detectat.")

    if "brave" in detected:
        report_chromium("BraveSoftware", "Brave-Browser")
    else:
        print("\n[SKIP] Brave no detectat.")

    if "opera" in detected:
        report_chromium("Opera Software", "Opera Stable")
        report_chromium("Opera Software", "Opera GX Stable")
    else:
        print("\n[SKIP] Opera no detectat.")

    # Firefox
    if "firefox" in detected:
        report_firefox()
    else:
        print("\n[SKIP] Firefox no detectat.")

    print("\n===== DIAGNÒSTIC FINALITZAT (NO S'HA ESBORRAT RES) =====")


if __name__ == "__main__":
    main()
