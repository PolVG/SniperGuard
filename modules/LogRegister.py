import os
from datetime import datetime
from pathlib import Path
from rich import *
from rich.console import *
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import configparser

'''
Aclariments generals sobre el sistema de logs: 
l'encoding utilitzat és UTF-8 per assegurar 
la compatibilitat amb caràcters especials i emojis.
'''

# Consola rich per a la sortida de text formatat
console = Console()

# Rutes de fitxers i directoris
BASE_DIR = Path(__file__).resolve().parent       
PROJECT_ROOT = BASE_DIR.parent     
LOGS_DIR = PROJECT_ROOT / "logs"
CONFIG_PATH = PROJECT_ROOT / "config" / "config.ini"
CURRENT_LOG_FILE = None


'''
AQUESTA FUNCIÓ ESTA FETA AMB IA


def _try_set_current_log_file_from_env():
Intenta establir el fitxer de log actual des de la variable d'entorn SNIPERGUARD_LOG_FILE.
Retorna True si s'ha establert correctament, False en cas contrari.

'''

def _try_set_current_log_file_from_env():
    global CURRENT_LOG_FILE

    env_path = os.environ.get("SNIPERGUARD_LOG_FILE")
    if not env_path:
        return False

    try:
        candidate = Path(env_path)
        candidate.parent.mkdir(parents=True, exist_ok=True)

        if not candidate.exists():
            with open(candidate, "a", encoding="utf-8"):
                pass

        CURRENT_LOG_FILE = candidate
        return True
    except Exception:
        return False

# LOG_LEVEL = 100  # Nivell mínim de logs a registrar
'''
get_current_log_file():
Retorna la ruta del fitxer de log actual.
'''
def get_current_log_file():    
    return CURRENT_LOG_FILE

'''
def get_time():
Retorna temps en format DD-MM-YYYY HH: MM:SS (per dins dels logs)
'''
def get_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
'''
def get_filename_time():
Retorna temps vàlid per a noms de fitxer (sense :  ni espais) ja que aquests caràcters poden causar problemes en alguns sistemes operatius com es Windows.
'''

def get_filename_time():
    return datetime.now().strftime("%d-%m-%Y_%H-%M-%S")


'''
def obtain_text_level(nivell: int):
Retorna l'etiqueta del nivell de log
'''
def obtain_text_level(nivell: int):
    
    nivells = {
        100: '[🔍 DEBUG]',
        200: '[ℹ️  INFO]',
        250: '[✅ NOTICE]',
        300: '[⚠️  WARNING]',
        400: '[❌ ERROR]',
    }
    return nivells.get(nivell, '[UNKNOWN]')


'''
def check_current_log_level(config_path=CONFIG_PATH) -> int:
Llegeix el paràmetre 'log_level_py' de la secció [log] del fitxer config.ini
Retorna el valor com a enter, o llança excepcions detallades si hi ha errors.


'''

def check_current_log_level(config_path=CONFIG_PATH) -> int:

    # Comprovem si el fitxer config.ini existeix
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"❌📄 ERROR! No s'ha trobat el fitxer: {config_path}")

    # Carreguem el fitxer INI amb el mòdul oficial 'configparser'
    config = configparser.ConfigParser()
    config.read(config_path)

    # Verifiquem que existeix la secció [log] dins del fitxer INI
    if 'log' not in config:
        raise Exception("❌📄 ERROR! Falta la secció [log] al fitxer 'config.ini'")

    # Verifiquem que existeix la clau 'log_level_py' dins de la secció [log]
    if 'log_level_py' not in config['log']:
        raise Exception("❌📄 ERROR! El paràmetre 'log_level_py' no està definit a la secció [log] del fitxer 'config.ini'")

    # Elimina espais en blanc si n'hi ha
    valor = config['log']['log_level_py'].strip()

    # Verifiquem que el valor no estigui buit
    if valor == '':
        raise Exception("❌📄 ERROR! El paràmetre 'log_level_py' està buit al fitxer 'config.ini'")

    # Al fitxer config-ini, guardem el valor del paràmetre com String.
    # Per tant, eliminem les cometes dobles del número i el castegem a INT
    # per poder decidir quin tipus de logs es mostren i quins no.
    # "200" = 200 -> Ara sí que podem convertir-lo de String a INT sense problemes.
    valor = valor.strip('"').strip("'")
    
 
    try:
        # Intentem convertir el valor a enter. Si no és possible, llancem un error
        return int(valor)
    except ValueError:
        raise Exception("❌📄 ERROR! El paràmetre 'log_level_py' no és un enter vàlid")

'''
def init_log_file():
Inicialitza el fitxer de log creant-lo i escrivint la capçalera inicial.
Retorna: La ruta del fitxer de log creat.
'''
def init_log_file():

    global CURRENT_LOG_FILE
    
    os.makedirs(LOGS_DIR, exist_ok=True)# Crear la carpeta de logs si no existeix, es gestiona amb exist_ok=True per evitar errors si ja existeix
    

    filename = f"{get_filename_time()}_logs_py.txt" # Nom del fitxer amb el temps de creacio
    CURRENT_LOG_FILE = LOGS_DIR / filename
    
    # Si el fitxer no existeix, crea'l i afegeix la capçalera avisant que el fitxer es nou
    with open(CURRENT_LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"[{get_time()}] ✅📝 Nou fitxer de log creat: {filename}\n")
        f.write(f"[{get_time()}] 🚀 Inici d'execució de SniperGuard\n")
        f.write("="*80 + "\n\n")
    
    return CURRENT_LOG_FILE



'''
def log(msg: str, nivell:  int = 200):
Registra un missatge al fitxer de log amb el nivell especificat.
Parametres:
msg: Missatge a registrar.   
nivell: Nivell de severitat del missatge (per defecte és 200 - INFO).
'''

def log(msg: str, nivell:  int = 200):
    try:
        nivell_permes = check_current_log_level()
    except Exception as e:
        print(e)
        return  # Atura el log si no es pot llegir el fitxer de configuració
    
    if nivell < nivell_permes:
        return # El nivell no arriba al mínim requerit
    
    if CURRENT_LOG_FILE is None:
        if not _try_set_current_log_file_from_env():
            init_log_file()
    
    text_nivell = obtain_text_level(nivell)
    full_msg = f"[{get_time()}] {text_nivell} {msg}"
    
    with open(CURRENT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")


# ---------- RICH: taula del baròmetre ---
LEVEL_STYLE = {
    100: "grey15",       # DEBUG
    200: "cyan",      # INFO
    250: "green",     # NOTICE
    300: "yellow",    # WARNING
    400: "bold red",  # ERROR
}


'''
def print_log_levels_table():
Mostra la taula del baròmetre. Si reps active_level, remarquem l'actiu.
Afegeix logs de depuració per saber que s'ha invocat correctament.
'''
def print_log_levels_table():
    log("Entrant a print_log_levels_table()", 100)
    print()

    table = Table(show_lines=True)

    panel = Panel(
        Align.center("[bold cyan underline] Baròmetre de Nivells de Log [/bold cyan underline]", vertical="middle"),
        border_style="green",
        style="on grey15",
        padding=(1, 6),
    )
    console.print(panel)

    log("Panell del barómetre mostrat correctament.", 100)

    table.add_column("ID", justify="right", no_wrap=True)
    table.add_column("Descripció", justify="left")

    log("Procedint a mostrar la taula.", 100)
    for lvl in (100, 200, 250, 300, 400):
        style = LEVEL_STYLE.get(lvl, "white")
        label = obtain_text_level(lvl)

        table.add_row(
            f"[{style}]{lvl}",
            f"[{style}]{label}",
       
        )
    console.print(table)
    log("Taula mostrada correctament.", 250)


'''
AQUESTA FUNCIÓ ESTA FETA AMB IA

def update_log_level_ini(new_level: int, config_path=CONFIG_PATH):
Actualitza el paràmetre 'log_level_py' al fitxer config.ini amb el nou nivell especificat.
Paràmetres:
new_level: Nou nivell de log a establir.
config_path: Ruta del fitxer config.ini (per defecte és CONFIG_PATH).

'''

  
def update_log_level_ini(new_level: int, config_path=CONFIG_PATH):
    
    # El fitxer config.ini amb els seus permisos, 
    # ja s'ha comprobat anteriorment amb el métode check_current_log_level()

    log(f"Inicialitzant 'update_log_level_ini()' amb el nivell: {new_level}", 100)
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
    config["log"]["log_level_py"] = f"\"{new_level}\""

    with open(config_path, "w", encoding="utf-8") as f:
        config.write(f)
    log("update_log_level_ini(): fitxer desat correctament.", 250)


'''
def manage_logs(current_log, new_log):
Actualitza el nivell mínim de logs a registrar segons la selecció de l'usuari.
choice: string validat (ex. "200", "300"...)    
new_log: nou nivell de log a establir
current_log: nivell de log actual abans del canvi


'''    

def manage_logs(current_log, new_log):

    log(f"Log escollit per l'usuari: {new_log}",250)
    update_log_level_ini(int(new_log))
    
    # Invoquem el nivell mínim de log que ha especificat l'usuari
    console.print(f"Nivell mínim de logs canviat per l'usuari: Antic: {current_log} Nou: {new_log}")
    
    # Recorda que aquest log no es mostrarà si hem agafat un baròemtre superior a 250
    log(f"Nivell mínim de logs canviat per l'usuari: Antic: {current_log} Nou: {new_log}", 250)
    

    
"""
EXPLICACIÓ DE LOGS

+------------+----------------+------------------------------------------+------------------------------+
| Nivell     | Valor numèric  | Descripció                               | Emoji i motiu               |
+------------+----------------+------------------------------------------+------------------------------+
| DEBUG      | 100            | Informació detallada de depuració        | 🔍 Lupa: s'està investigant |
| INFO       | 200            | Esdeveniments informatius (estat normal) | ℹ️ Informació estàndard     |
| NOTICE     | 250            | Esdeveniments normals però rellevants    | ✅ Tot correcte i notable   |
| WARNING    | 300            | Alguna cosa no ideal, però no crítica    | ⚠️ Precaució, pot empitjorar|
| ERROR      | 400            | Errors que impedeixen una acció          | ❌ Alguna cosa ha fallat    |
+------------+----------------+------------------------------------------+------------------------------+
"""