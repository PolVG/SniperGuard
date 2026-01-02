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


def get_timestamp():
    """Retorna timestamp en format DD-MM-YYYY HH: MM:SS (per dins dels logs)"""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def get_filename_timestamp():
    """Retorna timestamp vàlid per a noms de fitxer (sense :  ni espais)"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def obtain_text_level(nivell: int):
    """Retorna l'etiqueta del nivell de log"""
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


def init_log_file():
    """Crea un fitxer de log únic per a cada execució"""
    global CURRENT_LOG_FILE
    
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    # ✅ Utilitzar timestamp vàlid per a noms de fitxer
    filename = f"{get_filename_timestamp()}_logs_py.txt"
    CURRENT_LOG_FILE = LOGS_DIR / filename
    
    with open(CURRENT_LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"[{get_timestamp()}] ✅📝 Nou fitxer de log creat: {filename}\n")
        f.write(f"[{get_timestamp()}] 🚀 Inici d'execució de SniperGuard\n")
        f.write("="*80 + "\n\n")
    
    return CURRENT_LOG_FILE


def log(msg: str, nivell:  int = 200):
    """Registra un missatge de log amb un nivell específicat"""
    
    if nivell < LOG_LEVEL:
        return
    
    if CURRENT_LOG_FILE is None:
        init_log_file()
    
    text_nivell = obtain_text_level(nivell)
    full_msg = f"[{get_timestamp()}] {text_nivell} {msg}"
    
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