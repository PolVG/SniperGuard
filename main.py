import sys, os
import subprocess
import configparser
from pathlib import Path
from datetime import datetime
from modules.LogRegister import log
from recursos import check_input_user, check_admin_privileges

'''
--- Rutes absolutes globals ---
Fitxer: SniperGuard/pyapp/main.py  -> PROJECT_ROOT és SniperGuard/
'''

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

PYAPP_DIR = PROJECT_ROOT / "pyapp"

CONFIG_PATH = PROJECT_ROOT / "config" / "config.ini"
LOGS_DIR = PROJECT_ROOT / "logs"
MODULES_DIR = PROJECT_ROOT / "modules"

# Cada dia, es crea un nou fitxer de log.
LOG_FILE = LOGS_DIR / (datetime.now().strftime("%Y-%m-%d") + "_logs_py.txt")

# Opcions a escollir
MODE_BAR = 1  # identificar
MODE_DEL = 2  # identificar + esborrar


def get_config_ini():
    log(f"Inici get_config_ini(). CONFIG_PATH={CONFIG_PATH}", 100)

    config = configparser.ConfigParser()

    if not config.read(CONFIG_PATH, encoding="utf-8"):
        raise RuntimeError(f"No s'ha pogut llegir el fitxer INI: {CONFIG_PATH}")

    log(f"L'arxiu {CONFIG_PATH} s'ha trobat correctament.", 100)
    return config


def run_script(script_name: str):
    script_path = PYAPP_DIR / script_name

    if not script_path.exists():
        log(f"No existeix el fitxer: {script_path}", 400)
        return

    log(f"Preparant execució de script: {script_path}", 200)

    try:
        '''
        La creació de la estructura try-catch está fet amb IA, el que fa és executar un script Python
        des de un altre script Python, capturant la seva sortida (stdout i stderr)
        '''
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT)

        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=False,
            env=env,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if result.returncode == 0:
            log(f"Script {script_name} finalitzat OK (returncode=0)", 250)
        else:
            log(f"Script {script_name} ha acabat amb returncode={result.returncode}", 300)

        if result.stdout and result.stdout.strip():
            log(f"STDOUT {script_name}: {result.stdout.strip()}", 100)

        if result.stderr and result.stderr.strip():
            log(f"STDERR {script_name}: {result.stderr.strip()}", 400)

    except Exception as e:
        log(f"No s'ha pogut executar {script_name}: {(e)}", 500)


# ----------------------------
# NUEVO: entrada dedicada para GUI (sin consola)
# ----------------------------
def run_cleaning_from_gui(mode_choice: str, cleaning_choice: str):
    """
    Flujo paralelo para GUI.
    Cleaning es siempre la opción 2 del menú principal, así que aquí ejecutamos directamente
    el equivalente a: choose_mode() + cleaning_menu(mode) pero sin pedir input por consola.

    mode_choice: "1" (BAR) o "2" (DEL)
    cleaning_choice: "1"-"4"
    """
    log("Executant run_cleaning_from_gui() des de GUI", 200)

    # Mantener el check (si esto abre ventanas o imprime, dependerá de tu función)
    check_admin_privileges()

    if mode_choice not in {"1", "2"}:
        log(f"Mode inválid rebut des de GUI: {mode_choice}", 400)
        return

    mode = MODE_BAR if mode_choice == "1" else MODE_DEL

    bar_options = {
        "1": ("Estat arxius temporals", "BAR_test1_TEMP.py"),
        "2": ("Estat navegadors (historial/cookies/caché)", "BAR_test12_Full_Clean_browser.py"),
        "3": ("Estat paperera de reciclatge", "BAR_test4_Empty_Recycle_Bin.py"),
        "4": ("Tornar al menú", None),
    }

    del_options = {
        "1": ("Netejar arxius temporals", "DEL_test1_TEMP.py"),
        "2": ("Netejar navegadors (historial/cookies/caché)", "DEL_test12_Full_Clean_browser.py"),
        "3": ("Buidar paperera de reciclatge", "DEL_test4_Empty_Recycle_Bin.py"),
        "4": ("Tornar al menú", None),
    }

    options = bar_options if mode == MODE_BAR else del_options

    if cleaning_choice not in options:
        log(f"Opció cleaning inválida rebuda des de GUI: {cleaning_choice}", 400)
        return

    label, script = options[cleaning_choice]

    if script is None:
        log("Usuari torna al menú anterior (GUI)", 250)
        return

    log(f"Executant acció (GUI): {label}", 200)
    run_script(script)


def cleaning_menu(mode):
    log("Mostrant al usuari les opcions disponibles de neteja.", 100)

    BAR_OPTIONS = {
        "1": ("Estat arxius temporals", "BAR_test1_TEMP.py"),
        "2": ("Estat navegadors (historial/cookies/caché)", "BAR_test12_Full_Clean_browser.py"),
        "3": ("Estat paperera de reciclatge", "BAR_test4_Empty_Recycle_Bin.py"),
        "4": ("Tornar al menú", None),
    }

    DEL_OPTIONS = {
        "1": ("Netejar arxius temporals", "DEL_test1_TEMP.py"),
        "2": ("Netejar navegadors (historial/cookies/caché)", "DEL_test12_Full_Clean_browser.py"),
        "3": ("Buidar paperera de reciclatge", "DEL_test4_Empty_Recycle_Bin.py"),
        "4": ("Tornar al menú", None),
    }

    if mode == MODE_BAR:
        log("Mode BAR actiu: mostrant opcions de comprovació", 200)
        options = BAR_OPTIONS
    else:
        log("Mode DEL actiu: mostrant opcions de neteja", 200)
        options = DEL_OPTIONS

    print("\n***Cleaning Options:***\n")
    for key, (label, _) in options.items():
        print(f"{key}. {label}")
    print("\n")

    choice = check_input_user("Introdueix una opció : ", set(options.keys()))
    if choice is None:
        log("Sortint de la funció cleaning_menu()", 100)
        return

    log(f"L'usuari ha triat opció cleaning_menu: '{choice}' (mode={mode})", 200)

    label, script = options[choice]

    if script is None:
        log("Usuari torna al menú anterior", 250)
        return

    log(f"Executant acció: {label}", 200)
    run_script(script)


def hardening_menu(mode):
    log("Mostrant al usuari les opcions disponibles de hardening.", 100)

    BAR_OPTIONS = {
        "1": ("Comprobar si Windows Defender està actiu", "HARD_WinDefender.py"),
        "2": ("Comprobar si falten actualitzacions a Windows Defender", "HARD_WinDefenderUpdateAvailable.py"),
        "3": ("Comprobar si falten actualitzacions a Windows Update", "BAR_test5_UPDATE.py"),
        "4": ("Tornar al menú", None),
    }

    DEL_OPTIONS = {
        "1": ("Actualitzar Windows Defender", "HARD_WinDefenderUpdate.py"),
        "2": ("Actualizar Windows amb Windows Update", "HARD_WindowsUpdate.py"),
        "3": ("Tornar al menú", None),
    }

    if mode == MODE_BAR:
        log("Mode BAR actiu: mostrant opcions de comprovació", 200)
        options = BAR_OPTIONS
    else:
        log("Mode DEL actiu: mostrant opcions de neteja", 200)
        options = DEL_OPTIONS

    print("\n***Cleaning Options:***\n")
    for key, (label, _) in options.items():
        print(f"{key}. {label}")
    print("\n")

    choice = check_input_user("Introdueix una opció : ", set(options.keys()))
    if choice is None:
        log("Sortint de la funció cleaning_menu()", 100)
        return

    log(f"L'usuari ha triat opció cleaning_menu: '{choice}' (mode={mode})", 200)

    label, script = options[choice]

    if script is None:
        log("Usuari torna al menú anterior", 250)
        return

    log(f"Executant acció: {label}", 200)
    run_script(script)


def choose_mode():
    while True:
        print("Què vols fer?")
        print("1. Identificar estat (BAR)  -> només comprovar")
        print("2. Identificar i esborrar (DEL) -> comprovar + netejar")

        choice = check_input_user("Introdueix una opció : ", {"1", "2"})
        if choice is None:
            continue

        if choice == "1":
            log("Usuari ha seleccionat mode BAR", 250)
            return MODE_BAR

        log("Usuari ha seleccionat mode DEL", 250)
        return MODE_DEL


def choose_hardening_mode():
    while True:
        print("Què vols fer?")
        print("1. Identificar estat (BAR)  -> només comprovar")
        print("2. Implementar hardening (HARD) -> comprovar + hardening")

        choice = check_input_user("Introdueix una opció : ", {"1", "2"})
        if choice is None:
            continue

        if choice == "1":
            log("Usuari ha seleccionat mode BAR", 250)
            return MODE_BAR

        log("Usuari ha seleccionat mode HARD", 250)
        return MODE_DEL


def print_banner():
    log("Executant la funció 'print_banner()' per mostrar el banner inicial.", 100)
    print("\n")
    print("███████╗███╗   ██╗██╗██████╗ ███████╗██████╗  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗")
    print("██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗")
    print("███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝██║  ███╗██║   ██║███████║██████╔╝██║  ██║")
    print("╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║")
    print("███████║██║ ╚████║██║██║     ███████╗██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝")
    print("╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝")
    print("\n")


def main():
    while True:
        log("==== Starting SniperGuard  ====", 200)
        log(f"PROJECT_ROOT = {PROJECT_ROOT}", 100)
        log(f"BASE_DIR = {BASE_DIR}", 100)
        log(f"CONFIG_PATH = {CONFIG_PATH}", 100)
        log(f"LOGS_DIR = {LOGS_DIR}", 100)
        log(f"LOG_FILE({datetime.now().strftime('%Y-%m-%d')}) = {LOG_FILE}", 100)

        print_banner()
        print("-------------------------------")
        print("Welcome to SniperGuard!:")
        print("-------------------------------")

        check_admin_privileges()

        print("\n")
        print("Select an option:")
        print("1. Hardening")
        print("2. Cleaning")
        print("3. Exit")
        print("\n")

        decisio = check_input_user("Introdueix una opció : ", {"1", "2", "3"})
        if decisio is None:
            break

        if decisio == "1":
            log("Hardening seleccionat", 250)
            mode = choose_hardening_mode()
            hardening_menu(mode)
            break

        if decisio == "2":
            log("Cleaning seleccionat", 250)
            print("\n")
            mode = choose_mode()
            cleaning_menu(mode)
            break

        log("Usuari ha sortit del programa (Exit).", 200)
        break


if __name__ == "__main__":
    try:
        main()
        log("==== Fi SniperGuard (pyapp/main) ====", 200)
    except Exception as e:
        log(f"Error en la execució main: {(e)}", 600)