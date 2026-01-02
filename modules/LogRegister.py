import os
from datetime import datetime
from pathlib import Path

'''
Aclariments generals sobre el sistema de logs: 
l'encoding utilitzat és UTF-8 per assegurar la compatibilitat amb caràcters especials i emojis.
'''

BASE_DIR = Path(__file__).resolve().parent       
PROJECT_ROOT = BASE_DIR.parent     
LOGS_DIR = PROJECT_ROOT / "logs"

CURRENT_LOG_FILE = None
LOG_LEVEL = 100  # Nivell mínim de logs a registrar
'''
get_current_log_file():
Retorna la ruta del fitxer de log actual.
'''
def get_current_log_file():    
    return CURRENT_LOG_FILE

'''
def get_time():
Retorna temps en format DD-MM-YYYY HH: MM:SS (per dins dels logs
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
        200: '[ℹ️ INFO]',
        250: '[✅ NOTICE]',
        300: '[⚠️ WARNING]',
        400: '[❌ ERROR]',
        500: '[🛑 CRITICAL]',
        550: '[🚨 ALERT]',
        600: '[☠️ EMERGENCY]',
    }
    return nivells. get(nivell, '[UNKNOWN]')

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
 
    
    if nivell < LOG_LEVEL:
        return
    
    if CURRENT_LOG_FILE is None:
        init_log_file()
    
    text_nivell = obtain_text_level(nivell)
    full_msg = f"[{get_time()}] {text_nivell} {msg}"
    
    with open(CURRENT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")


"""
EXPLICACIÓ DE LOGS

+------------+----------------+------------------------------------------+------------------------------+
| Nivell     | Valor numèric  | Descripció                               | Emoji i motiu               |
+------------+----------------+------------------------------------------+------------------------------+
| DEBUG      | 100            | Informació detallada de depuració        | 🔍 Lupa: s'està investigant |
| INFO       | 200            | Esdeveniments informatius (estat normal) | ℹ️ Informació estàndard     |
| NOTICE     | 250            | Esdeveniments normals però rellevants    | ✅ Tot correcte i notable   |
| WARNING    | 300            | Alguna cosa no ideal, però no crítica    | ⚠️ Precaució, pot empitjorar|
| ERROR      | 400            | Errors que impedeixen una acció          | ❌ Alguna cosa ha fallat     |
| CRITICAL   | 500            | Problema greu, cal atenció immediata     | 🛑 Crítica fallada          |
| ALERT      | 550            | S'ha de resoldre immediatament           | 🚨 Alarma, acció urgent     |
| EMERGENCY  | 600            | El sistema és inutilitzable              | ☠️ Perill extrem, tot cau   |
+------------+----------------+------------------------------------------+------------------------------+
"""