import sys, os
import subprocess
import configparser
from pathlib import Path
from datetime import datetime
from modules.LogRegister import log


# --- Rutes absolutes globals ---
# Fitxer: SniperGuard/pyapp/main.py  -> PROJECT_ROOT és SniperGuard/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
PY_DIR = os.path.join(PROJECT_ROOT, "pyapp")
print(PROJECT_ROOT)

BASE_DIR = Path(__file__).resolve().parent  # SniperGuard/pyapp

CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "config.ini")
print(CONFIG_PATH)

LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
MODULES_DIR = os.path.join(PROJECT_ROOT, "modules")

# Cada dia, es crea un nou fitxer de log.
LOG_FILE = os.path.join(LOGS_DIR, datetime.now().strftime("%Y-%m-%d") + "_logs_py.txt")

# assegurar carpeta logs
os.makedirs(LOGS_DIR, exist_ok=True)


#
# get_config_ini()
#
def get_config_ini():
    log(f"Inici get_config_ini(). CONFIG_PATH={CONFIG_PATH}", 100)
    
    # Leer el fichero de configuración "config.ini" (barómetro de los logs)
    config = configparser.ConfigParser()
    if not config.read(CONFIG_PATH, encoding="utf-8"):
        raise RuntimeError(f"No s'ha pogut llegir el fitxer INI: {CONFIG_PATH}")
    
    log(f"L'arxiu {CONFIG_PATH} s'ha trobat correctament.", 100)
    


def run_script(script_name: str):
    """
    Executa un script Python del projecte (BAR_*.py o DEL_*.py)
    utilitzant el mateix interpreter (sys.executable).
    Opció 1: injecta PYTHONPATH perquè els scripts importin modules.*
    """
    script_path = BASE_DIR / PY_DIR / script_name
    log(f"Preparant execució de script: {script_name} | path={script_path}", 200)

    # Verifica si l'script de Python que realitza aquella funcionalitat existeix.
    if not script_path.exists():
        log(f"No existeix el fitxer: {script_path}", 400)
        return

    # Si existeix, executa aquell arxiu i guarda el seu 'output' als logs.
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = PROJECT_ROOT  

        result = subprocess.run(
            [sys.executable, 
            str(script_path)],
            check=False,
            env=env,
            cwd=PROJECT_ROOT,       
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        # Si el fitxer s'executa correctament, l'script retorna 0.
        if result.returncode == 0:
            print(f"Script {script_name} finalitzat OK (returncode=0)", 250)
        else:
            print(f"Script {script_name} ha acabat amb returncode={result.returncode}", 300)

        # Necessitem capturar la sortida del script per guadar el seu comportament als logs
        
        if result.stdout and result.stdout.strip(): # TOT OK
            print(f"STDOUT {script_name}: {result.stdout.strip()}", 100)

        if result.stderr and result.stderr.strip(): # ERROR!
            print(f"STDERR {script_name}: {result.stderr.strip()}", 400)

    except Exception as e:
        log(f"No s'ha pogut executar {script_name}: {(e)}", 500)





# Funció que serveix per mostrar al usuari les opcions de neteja del menú.
def cleaning_menu(mode):
    log(f"Mostrant al usuari les opcions disponibles de neteja.", 100)

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
    
    # Esborrem espais a la dreta i a l'esquerra
    # per treballar amb un input net.
    choice = input("Introdueix una opció : ").strip()
    log(f"Usuari ha triat opció cleaning_menu: '{choice}' (mode={mode})", 200)
    
    # Si l'entrada de l'usuari està buida. Torna al menú principal
    if not choice:
        log("La entrada del usuari es buida. Introdueix un número d'1-4.",400)
        
    # Si no es pas un dígit (0-9). Torna al menú principal
    if not choice.isdigit():
        log("\nLa entrada del usuari no es pas un dígit. Introdueix un número d'1-4.",400)

    # Convertim de String a Integer per revisar
    # si el número del usuari està dintre del rang.
    choice = int(choice) 

    action = options.get(choice)

    if action:
        if 1 <= choice <= 4:
            if choice == 4:
                log("Usuari torna al menú anterior", 250)
                return

        log(f"Executant acció: {action[0]}", 200)
        action[1]()  # executa la funció
    else:
        #log(f"Opció invàlida a cleaning_menu(): '{choice}'", 300)
        print(f"Opció {choice} no valida.\n")

# Permet que l'suari escolleixi entre identificar l'entorn, 
# o bé: identificar i esborrar
def choose_mode():

    while True:
        print("Què vols fer?")
        print("1. Identificar estat (BAR)  -> només comprovar")
        print("2. Identificar i esborrar (DEL) -> comprovar + netejar")
        choice = input("Introdueix una opció : ").strip()
        
        # Si l'entrada de l'usuari està buida. Torna al menú principal
        if not choice:
            log("La entrada del usuari es buida. Introdueix un número d'1-4.",400)
        
        # Si no es pas un dígit (0-9). Torna al menú principal
        if not choice.isdigit():
            log("\nLa entrada del usuari no es pas un dígit. Introdueix un número d'1-4.",400)

        # Convertim de String a Integer per revisar
        # si el número del usuari està dintre del rang.
        choice = int(choice) 
        
        if choice == 1:
            log("Usuari ha seleccionat mode BAR", 250)
            return "BAR"
        else:
            log("Usuari ha seleccionat mode DEL", 250)
            return "DEL"

# Imprimim el banner
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


# Inicialitzem el menú principal
def main():
    while True:
        # Troubleshooting
        # Guardem com a log les rutes amb les que treballa el programa
        log("==== Starting SniperGuard  ====", 200)
        log(f"PROJECT_ROOT = {PROJECT_ROOT}", 100)
        log(f"BASE_DIR = {BASE_DIR}", 100)
        log(f"CONFIG_PATH = {CONFIG_PATH}", 100)
        log(f"LOGS_DIR = {LOGS_DIR}", 100)
        
        # Cada dia es genera un arxiu de log diferent.
        log(f"LOG_FILE({datetime.now().strftime('%Y-%m-%d')}) = {LOG_FILE}", 100)


        print_banner()
        print("-------------------------------")
        print("Welcome to SniperGuard!:")
        print("-------------------------------")

        print("\n")
        print("Select an option:")
        print("1. Hardening (Coming soon)")
        print("2. Cleaning")

        # Esborrem espais a la dreta i a l'esquerra
        # per treballar amb un input net.
        decisio = input("Introdueix una opció : ").strip()

        # Si l'entrada de l'usuari està buida. Torna al menú principal
        if not decisio:
            log("La entrada del usuari es buida. Introdueix un número d'1-4.",400)
            continue
        
        # Si no es pas un dígit (0-9). Torna al menú principal
        if not decisio.isdigit():
            log("\nLa entrada del usuari no es pas un dígit. Introdueix un número d'1-4.",400)
            continue

        # Convertim de String a Integer per revisar
        # si el número del usuari està dintre del rang.
        decisio = int(decisio) 
        
        if decisio not in (1,2): # 1 - 2
            # Numero incorrecte, NO està en el menú.-
            log(f"El número: {decisio} no està dintre del rang. El número ha de ser d'1-2.",400)
            continue

        if decisio == 1:
            log("Hardening seleccionat (no implementat)", 300)  
        else:
            log("Cleaning seleccionat", 250)
            print("\n")
            
            # L'usuari ha d'escollir un mode: identificar o identificar + esborrar.
            mode = choose_mode()

            # Mostra les opcions de neteja de SniperGuard
            cleaning_menu(mode)
     
      
# Inicilitzem SniperGuard
# Totes les excepcions han de quedar controlades
if __name__ == "__main__":
    try:
        main()
        log("==== Fi SniperGuard (pyapp/main) ====", 200)
    except Exception as e:
        log(f"Excepció no controlada a __main__: {(e)}", 600)