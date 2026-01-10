"""
TOT EL CONTINGUT D'AQUEST SCRIPT ESTA FET AMB IA. EN LA SEGUENT ENTREGA ES SUBSTITUIRA PER CODI HUMÀ.
"""

import os
import getpass
from pathlib import Path
from modules.LogRegister import log


# =========================================================
# CONFIGURACIÓ BARÒMETRE
# =========================================================

URGENT_SIZE_MB = 2048      # > 2 GB
URGENT_FILES = 20000

RECOMMENDED_SIZE_MB = 500 # > 500 MB
RECOMMENDED_FILES = 5000


# =========================================================
# UTILITATS
# =========================================================

def calcular_mida_i_fitxers(ruta: Path):
    """
    Calcula mida total (bytes) i nombre de fitxers dins una carpeta.
    NO segueix symlinks.
    """
    ruta = Path(ruta)

    log(f"Inici càlcul mida i fitxers: {ruta}", 100)

    total_size = 0
    total_files = 0

    for root, dirs, files in os.walk(ruta, followlinks=False):
        total_files += len(files)

        for f in files:
            fp = Path(root) / f
            try:
                total_size += fp.stat().st_size
            except Exception as e:
                # Error puntual: no atura execució
                log(
                    f"No s'ha pogut accedir a fitxer: {fp} ({repr(e)})",
                    300
                )
                continue

    log(
        f"Càlcul finalitzat: ruta={ruta} | bytes={total_size} | fitxers={total_files}",
        100
    )

    return total_size, total_files


def barometre(size_mb, file_count):
    """
    Retorna (color, text) segons criteris.
    """
    log(
        f"Avaluant baròmetre: size_mb={size_mb}, file_count={file_count}",
        100
    )

    if size_mb >= URGENT_SIZE_MB or file_count >= URGENT_FILES:
        log("Estat URGENT detectat", 300)
        return "[RED]", "URGENT (molt recomanat netejar)"

    elif size_mb >= RECOMMENDED_SIZE_MB or file_count >= RECOMMENDED_FILES:
        log("Estat RECOMANABLE detectat", 250)
        return "[YELLOW]", "RECOMANABLE"

    else:
        log("Estat OK (no cal netejar)", 200)
        return "[GREEN]", "NO CAL, però es pot netejar"


def analitzar_carpeta(nom, ruta_str):
    ruta = Path(ruta_str)

    log(f"Inici anàlisi carpeta: {nom} | ruta={ruta}", 200)

    print(f"\n===== {nom.upper()} =====")
    print(f"Ruta: {ruta}")

    if not ruta.exists():
        log(f"La ruta no existeix: {ruta}", 300)
        print("WARNING: No existeix.")
        return

    if not ruta.is_dir():
        log(f"La ruta no és una carpeta: {ruta}", 300)
        print("WARNING: No és una carpeta.")
        return

    size_bytes, file_count = calcular_mida_i_fitxers(ruta)
    size_mb = round(size_bytes / (1024 * 1024), 2)

    color, estat = barometre(size_mb, file_count)

    log(
         f"Resultat carpeta '{nom}': size_mb={size_mb}, files={file_count}, estat={estat}",
         200
    )

    print(f"Mida total : {size_mb} MB")
    print(f"Fitxers    : {file_count}")
    print(f"Baròmetre  : {color} {estat}")


# =========================================================
# ANALISI CARPETES SISTEMA
# =========================================================

def analitzar_carpetes_sistema():
    log("Inici anàlisi carpetes del sistema", 200)

    # 1) C:\Windows\Temp
    carpeta_windows_temp = Path(r"C:\Windows\Temp")

    # 2) C:\Windows\SoftwareDistribution\Download
    carpeta_software_distribution = Path(r"C:\Windows\SoftwareDistribution\Download")

    # 3) C:\Users\%username%\AppData\Local\Temp
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        carpeta_usuario_temp = Path(local_appdata) / "Temp"
        log(f"LOCALAPPDATA detectat: {local_appdata}", 100)
    else:
        usuario = getpass.getuser()
        carpeta_usuario_temp = Path(fr"C:\Users\{usuario}\AppData\Local\Temp")
        log(
             f"LOCALAPPDATA no definit. Usuari detectat via getpass: {usuario}",
             300
        )

    print("\n========== ANÀLISI CARPETES DEL SISTEMA ==========")

    analitzar_carpeta("Windows Temp", carpeta_windows_temp)
    analitzar_carpeta("Windows Update Download", carpeta_software_distribution)
    analitzar_carpeta("Temp Usuari", carpeta_usuario_temp)

    log("Final anàlisi carpetes del sistema", 200)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    try:
        log("==== Inici diagnòstic Windows (BAR mode segur) ====", 200)

        print("===== DIAGNÒSTIC WINDOWS (MODE SEGUR - NO ESBORRA RES) =====")
        analitzar_carpetes_sistema()
        print("\n===== ANÀLISI FINALITZADA =====")

        log("Diagnòstic Windows finalitzat correctament", 250)

    except Exception as e:
        # Norma del projecte: cap error sense log
        log(f"Excepció no controlada al diagnòstic Windows: {repr(e)}", 600)
        raise