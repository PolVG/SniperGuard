# llibreries externes
import sys, os
import subprocess
import configparser
from pathlib import Path
from datetime import datetime

# llibreries internes
from modules.LogRegister import log
from recursos import check_input_user, check_admin_privileges


# Definició de rutes globals
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

PYAPP_DIR = PROJECT_ROOT / "pyapp"
CONFIG_PATH = PROJECT_ROOT / "config" / "config.ini"
LOGS_DIR = PROJECT_ROOT / "logs"
MODULES_DIR = PROJECT_ROOT / "modules"

# Cada dia, es crea un nou fitxer de log.
LOG_FILE = LOGS_DIR / (datetime.now().strftime("%Y-%m-%d") + "_logs_py.txt")

MODE_BAR = 1  # identificar
MODE_DEL = 2  # identificar + esborrar


'''
def get_config_ini():
Aquesta funció llegeix i retorna la configuració des d'un fitxer INI.
'''
def get_config_ini():
    log(f"Inici get_config_ini(). CONFIG_PATH={CONFIG_PATH}", 100)

    config = configparser.ConfigParser()


    if not config.read(CONFIG_PATH, encoding="utf-8"):
        raise RuntimeError(f"No s'ha pogut llegir el fitxer INI: {CONFIG_PATH}")

    log(f"L'arxiu {CONFIG_PATH} s'ha trobat correctament.", 100)
    return config


'''
def run_script(script_name: str):
Aquesta funció s'utilitza per executar un script Python específic des de la ubicació PYAPP_DIR.
Rep com a paràmetre el nom de l'script i gestiona la seva execució, capturant la sortida i els errors.
'''
def run_script(script_name: str):
    script_path = PYAPP_DIR / script_name

    if not script_path.exists():
        log(f"No existeix el fitxer: {script_path}", 400)
        return

    if not sys.executable:
        log("sys.executable no està disponible. No es pot executar subprocess.", 500)
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
            timeout=300, 
        )

        if result.returncode == 0:
            log(f"Script {script_name} finalitzat OK (returncode=0)", 250)
        else:
            log(f"Script {script_name} ha acabat amb returncode={result.returncode}", 300)

        if result.stdout and result.stdout.strip():
            log(f"STDOUT {script_name}: {result.stdout.strip()}", 100)

        if result.stderr and result.stderr.strip():
            log(f"STDERR {script_name}: {result.stderr.strip()}", 400)

    except subprocess.TimeoutExpired:
        log(f"Timeout executant {script_name}. El procés ha trigat massa.", 500)
        print("Error: el procés ha trigat massa i s'ha aturat.")
    except Exception as e:
        log(f"No s'ha pogut executar {script_name}: {(e)}", 500)


'''
def run_cleaning_from_gui(mode_choice: str, cleaning_choice: str):
Aquesta funció s'utilitza per executar les operacions de neteja des de la interfície gràfica d'usuari (GUI).
Rep com a paràmetres les opcions seleccionades per l'usuari a la GUI i executa l'script corresponent segons aquestes opcions.
'''
def run_cleaning_from_gui(mode_choice: str, cleaning_choice: str):
    log("Executant run_cleaning_from_gui() des de GUI", 200)

    try:
        check_admin_privileges()
    except Exception as e:
        log(f"Error en check_admin_privileges() (GUI): {e}", 600)
        return

    if mode_choice not in {"1", "2"}:
        log(f"Mode invàlid rebut des de GUI: {mode_choice}", 400)
        return

    mode = MODE_BAR if mode_choice == "1" else MODE_DEL

    bar_options = {
        "1": ("Estat arxius temporals", "BAR_test1_TEMP.py"),
        "2": ("Estat navegadors (historial/cookies/caché)", "BAR_test12_Full_Clean_browser.py"),
        "3": ("Estat paperera de reciclatge", "BAR_test4_Empty_Recycle_Bin.py"),
    }

    del_options = {
        "1": ("Netejar arxius temporals", "DEL_test1_TEMP.py"),
        "2": ("Netejar navegadors (historial/cookies/caché)", "DEL_test12_Full_Clean_browser.py"),
        "3": ("Buidar paperera de reciclatge", "DEL_test4_Empty_Recycle_Bin.py"),
    }

    options = bar_options if mode == MODE_BAR else del_options

    if cleaning_choice not in options:
        log(f"Opció cleaning invàlida rebuda des de GUI: {cleaning_choice}", 400)
        return

    label, script = options[cleaning_choice]
    log(f"Executant acció (GUI): {label}", 200)
    run_script(script)


'''
def cleaning_menu(mode):
Aquesta funció mostra un menú de neteja a l'usuari i executa l'script corresponent segons la seva elecció.
'''
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
        "4": ("Realitzar una neteja ràpida amb 'cleanmgr.exe'", "DEL_cleanmgr_fast.py"),
        # "5": ("Realitzar una neteja lenta amb 'cleanmgr.exe'", "DEL_cleanmgr_slow.py"),
        "5": ("Tornar al menú", None),
    }

    if mode == MODE_BAR:
        log("Mode BAR actiu: mostrant opcions de comprovació", 200)
        options = BAR_OPTIONS
    else:
        log("Mode DEL actiu: mostrant opcions de neteja", 200)
        options = DEL_OPTIONS

    print("\n***Opcions Cleaning:***\n")
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


'''
def hardening_menu(mode):
Aquesta funció mostra un menú de hardening a l'usuari i executa l'script corresponent segons la seva elecció.
'''
def hardening_menu(mode):
    log("Mostrant al usuari les opcions disponibles de hardening.", 100)

    BAR_OPTIONS = {
        "1": ("Comprovar si Windows Defender està actiu", "HARD_WinDefender.py"),
        "2": ("Comprovar si falten actualitzacions a Windows Defender", "HARD_WinDefenderUpdateAvailable.py"),
        "3": ("Comprovar si falten actualitzacions a Windows Update", "BAR_test5_UPDATE.py"),
        "4": ("Tornar al menú", None),
    }

    DEL_OPTIONS = {
        "1": ("Actualitzar Windows Defender", "HARD_WinDefenderUpdate.py"),
        "2": ("Actualitzar Windows amb Windows Update", "HARD_WindowsUpdate.py"),
        "3": ("Tornar al menú", None),
    }

    if mode == MODE_BAR:
        log("Mode BAR actiu: mostrant opcions de comprovació", 200)
        options = BAR_OPTIONS
    else:
        log("Mode DEL actiu: mostrant opcions de neteja", 200)
        options = DEL_OPTIONS

    print("\n***Opcions Hardening:***\n")
    for key, (label, _) in options.items():
        print(f"{key}. {label}")
    print("\n")

    choice = check_input_user("Introdueix una opció : ", set(options.keys()))
    if choice is None:
        log("Sortint de la funció hardening_menu()", 100)
        return

    log(f"L'usuari ha triat opció hardening_menu: '{choice}' (mode={mode})", 200)

    label, script = options[choice]

    if script is None:
        log("Usuari torna al menú anterior", 250)
        return

    log(f"Executant acció: {label}", 200)
    run_script(script)


'''
def choose_mode():
Aquesta funció demana a l'usuari que triï entre dos modes: BAR (només comprovar) o DEL (comprovar + esborrar).
'''
def choose_mode():
    attempts = 0
    while True:
        print("Què vols fer?")
        print("1. Identificar estat (BAR)  -> només comprovar")
        print("2. Identificar i esborrar (DEL) -> comprovar + netejar")

        try:
            choice = check_input_user("Introdueix una opció : ", {"1", "2"})
        except Exception as e:
            log(f"Error en check_input_user() dins choose_mode(): {e}", 600)
            choice = None

        if choice is None:
            attempts += 1
            if attempts >= 3:
                log("Massa intents fallits a choose_mode(). Tornant al menú principal.", 400)
                return None
            print("Entrada no vàlida. Reintenta-ho.")
            continue

        if choice == "1":
            log("Usuari ha seleccionat mode BAR", 250)
            return MODE_BAR

        log("Usuari ha seleccionat mode DEL", 250)
        return MODE_DEL


'''
def choose_hardening_mode():
Aquesta funció demana a l'usuari que triï entre dos modes de hardening: BAR (només comprovar) o HARD (comprovar + hardening).
'''
def choose_hardening_mode():
    attempts = 0
    while True:
        print("Què vols fer?")
        print("1. Identificar estat (BAR)  -> només comprovar")
        print("2. Implementar hardening (HARD) -> comprovar + hardening")

        try:
            choice = check_input_user("Introdueix una opció : ", {"1", "2"})
        except Exception as e:
            log(f"Error en check_input_user() dins choose_hardening_mode(): {e}", 600)
            choice = None

        if choice is None:
            attempts += 1
            if attempts >= 3:
                log("Massa intents fallits a choose_hardening_mode(). Tornant al menú principal.", 400)
                return None
            print("Entrada no vàlida. Reintenta-ho.")
            continue

        if choice == "1":
            log("Usuari ha seleccionat mode BAR", 250)
            return MODE_BAR

        log("Usuari ha seleccionat mode HARD", 250)
        return MODE_DEL


'''
def print_banner():
Aquesta funció imprimeix un banner inicial de SniperGuard a la consola.
'''
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


'''
def main():
Aquesta funció gestiona el flux principal del programa SniperGuard.
Mostra un menú a l'usuari per triar entre les opcions de Hardening, Cleaning o sortir del programa.
'''
def main():
    while True:
        log("==== SNIPERGUARD iniciant  ====", 200)
        log(f"PROJECT_ROOT = {PROJECT_ROOT}", 100)
        log(f"BASE_DIR = {BASE_DIR}", 100)
        log(f"CONFIG_PATH = {CONFIG_PATH}", 100)
        log(f"LOGS_DIR = {LOGS_DIR}", 100)
        log(f"LOG_FILE({datetime.now().strftime('%Y-%m-%d')}) = {LOG_FILE}", 100)

        print_banner()
        print("-------------------------------")
        print("             Menú              ")
        print("-------------------------------")

        try:
            check_admin_privileges()
        except Exception as e:
            log(f"Error en check_admin_privileges(): {e}", 600)
            print("Error: no es van poder comprovar els privilegis d'administrador.")
            break

        attempts = 0
        while True:
            print("Escolleix una opció:")
            print("1. Hardening")
            print("2. Cleaning")
            print("3. Sortir")
            print("\n")

            try:
                decisio = check_input_user("Introdueix una opció : ", {"1", "2", "3"})
            except Exception as e:
                log(f"Error en check_input_user(): {e}", 600)
                decisio = None

            if decisio is None:
                attempts += 1
                if attempts >= 3:
                    log("Massa intents fallits al menú principal. Sortint.", 400)
                    return
                print("Entrada no vàlida. Torna-ho a provar.")
                continue

            if decisio == "1":
                log("Hardening seleccionat", 250)
                try:
                    mode = choose_hardening_mode()
                    if mode is None:
                        break
                    hardening_menu(mode)
                except Exception as e:
                    log(f"Error executant Hardening: {e}", 600)
                    print("Error executant Hardening. Revisa els logs.")
                break

            if decisio == "2":
                log("Cleaning seleccionat", 250)
                print("\n")
                try:
                    mode = choose_mode()
                    if mode is None:
                        break
                    cleaning_menu(mode)
                except Exception as e:
                    log(f"Error executant Cleaning: {e}", 600)
                    print("Error executant Cleaning. Revisa els logs.")
                break

            log("Usuari ha sortit del programa (Exit).", 200)
            return


if __name__ == "__main__":
    try:
        main()
        log("==== Fi SniperGuard (pyapp/main) ====", 200)
    except Exception as e:
        log(f"Error en la execució main: {(e)}", 600)