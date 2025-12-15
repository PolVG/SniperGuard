import sys, os
import subprocess
import configparser
from pathlib import Path
from datetime import datetime
from modules.LogRegister import log


# --- Rutes absolutes globals ---
# Fitxer: SniperGuard/pyapp/main.py  -> PROJECT_ROOT és SniperGuard/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(PROJECT_ROOT)
BASE_DIR = Path(__file__).resolve().parent  # SniperGuard/pyapp

CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "config.ini")
print(CONFIG_PATH)
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")

# Cada dia, es crea un nou fitxer de log.
LOG_FILE = os.path.join(LOGS_DIR, datetime.now().strftime("%Y-%m-%d") + "_logs_py.txt")

# assegurar carpeta logs
os.makedirs(LOGS_DIR, exist_ok=True)


#
# get_pyauto_username_from_ini()
#
def get_pyauto_username_from_ini() -> str:
    log(f"Inici get_pyauto_username_from_ini(). CONFIG_PATH={CONFIG_PATH}", 100)

    config = configparser.ConfigParser()
    if not config.read(CONFIG_PATH, encoding="utf-8"):
        # norma: log() + raise
        log(f"No s'ha pogut llegir el fitxer INI: {CONFIG_PATH}", 400)
        raise RuntimeError(f"❌ No s'ha pogut llegir el fitxer INI: {CONFIG_PATH}")

    if "intern" not in config or "PYAUTOusername" not in config["intern"]:
        log("Falta [intern].PYAUTOusername al fitxer INI", 400)
        raise RuntimeError("❌ Falta [intern].PYAUTOusername al fitxer INI")

    username = config["intern"]["PYAUTOusername"].strip().strip('"').strip("'")
    log(f"PYAUTOusername llegit correctament: {username}", 250)
    return username


def run_script(script_name: str) -> None:
    """
    Executa un script Python del projecte (BAR_*.py o DEL_*.py)
    utilitzant el mateix interpreter (sys.executable).
    Opció 1: injecta PYTHONPATH perquè els scripts importin modules.*
    """
    script_path = BASE_DIR / script_name
    log(f"Preparant execució de script: {script_name} | path={script_path}", 200)

    if not script_path.exists():
        log(f"No existeix el fitxer: {script_path}", 400)
        print(f"[ERROR] No existeix el fitxer: {script_path}")
        return

    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = PROJECT_ROOT  

        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=False,
            env=env,
            cwd=PROJECT_ROOT,       
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        # Log del resultat
        if result.returncode == 0:
            log(f"Script {script_name} finalitzat OK (returncode=0)", 250)
        else:
            log(f"Script {script_name} ha acabat amb returncode={result.returncode}", 300)

        # Captura de sortida (debug/error)
        if result.stdout and result.stdout.strip():
            log(f"STDOUT {script_name}: {result.stdout.strip()}", 100)

        if result.stderr and result.stderr.strip():
            log(f"STDERR {script_name}: {result.stderr.strip()}", 400)

    except Exception as e:
        log(f"No s'ha pogut executar {script_name}: {repr(e)}", 500)
        print(f"[ERROR] No s'ha pogut executar {script_name}: {e}")


def print_banner() -> None:
    log("Mostrant banner inicial", 100)
    print("\n")
    print("███████╗███╗   ██╗██╗██████╗ ███████╗██████╗  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗")
    print("██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗")
    print("███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝██║  ███╗██║   ██║███████║██████╔╝██║  ██║")
    print("╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║")
    print("███████║██║ ╚████║██║██║     ███████╗██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝")
    print("╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝")
    print("\n")


def choose_mode() -> str:
    log("Entrant a choose_mode()", 100)

    while True:
        print("Què vols fer?")
        print("1. Identificar estat (BAR)  -> només comprovar")
        print("2. Identificar i esborrar (DEL) -> comprovar + netejar")
        mode = input("> ").strip()

        if mode == "1":
            log("Usuari ha seleccionat mode BAR", 250)
            return "BAR"
        if mode == "2":
            log("Usuari ha seleccionat mode DEL", 250)
            return "DEL"

        log(f"Opció invàlida a choose_mode(): '{mode}'", 300)
        print("Opció invàlida. Torna-ho a provar.\n")


def cleaning_menu(mode: str) -> None:
    log(f"Inici cleaning_menu(mode={mode})", 100)

    # --- Diccionaris separats ---
    BAR_OPTIONS = {
        "1": ("Estat arxius temporals", lambda: run_script("BAR_test1_TEMP.py")),
        "2": ("Estat navegadors (historial/cookies/caché)", lambda: run_script("BAR_test12_Full_Clean_browser.py")),
        "3": ("Estat paperera de reciclatge", lambda: run_script("BAR_test4_Empty_Recycle_Bin.py")),
        "4": ("Tornar al menú", lambda: None),
    }

    DEL_OPTIONS = {
        "1": ("Netejar arxius temporals", lambda: run_script("DEL_test1_TEMP.py")),
        "2": ("Netejar navegadors (historial/cookies/caché)", lambda: run_script("DEL_test12_Full_Clean_browser.py")),
        "3": ("Buidar paperera de reciclatge", lambda: run_script("DEL_test4_Empty_Recycle_Bin.py")),
        "4": ("Tornar al menú", lambda: None),
    }

    options = BAR_OPTIONS if mode == "BAR" else DEL_OPTIONS

    print("\n***Cleaning Options:***\n")
    for key, (label, _) in options.items():
        print(f"{key}. {label}")

    print("\n")
    choice = input("> ").strip()
    log(f"Usuari ha triat opció cleaning_menu: '{choice}' (mode={mode})", 200)

    action = options.get(choice)
    if action:
        if choice == "4":
            log("Usuari torna al menú anterior", 250)
            return

        log(f"Executant acció: {action[0]}", 200)
        action[1]()  # executa la funció
    else:
        log(f"Opció invàlida a cleaning_menu(): '{choice}'", 300)
        print("Opció invàlida.\n")


def main():
    while True:
        log("==== Inici SniperGuard (pyapp/main) ====", 200)
        log(f"PROJECT_ROOT={PROJECT_ROOT}", 100)
        log(f"BASE_DIR={BASE_DIR}", 100)
        log(f"CONFIG_PATH={CONFIG_PATH}", 100)
        log(f"LOGS_DIR={LOGS_DIR}", 100)
        log(f"LOG_FILE(today)={LOG_FILE}", 100)

        print_banner()
        log("Initializing SniperGuard...", 200)
        print("Initializing SniperGuard...\n")
        print("Options:\n")
        print("1. Hardening (Not yet implemented)")
        print("2. Cleaning")

        option = input("> ").strip()
        log(f"Usuari ha triat opció principal: '{option}'", 200)

        if option == "1":
            log("Hardening seleccionat (no implementat)", 300)
            print("Hardening module is not yet implemented.")
            continue

        elif option == "2":
            log("Cleaning seleccionat", 250)
            print("\n")
            mode = choose_mode()
            cleaning_menu(mode)
            log("Sortint del mòdul Cleaning", 250)
            continue

        else:
            log(f"Opció invàlida al menú principal: '{option}'", 300)
            print("Opció invàlida.")
            continue



if __name__ == "__main__":
    try:
        main()
        log("==== Fi SniperGuard (pyapp/main) ====", 200)
    except Exception as e:
        # Cap error pot escapar sense log
        log(f"Excepció no controlada a __main__: {repr(e)}", 600)
        raise