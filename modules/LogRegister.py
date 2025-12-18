import os
import inspect
import re
import configparser
from datetime import datetime
from pathlib import Path

# Rutes globals del fitxer de logs
# Pujem dos nivells de l'arrel del projecte per oferir la ruta: /var/www/html/projecteimatges/config/config.ini
# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
# LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
# LOG_FILE = os.path.join(LOGS_DIR, datetime.now().strftime("%Y-%m-%d") + "_logs_py.txt")
# CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "config.ini")
BASE_DIR = Path(__file__).resolve().parent       
PROJECT_ROOT = BASE_DIR.parent     
LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOGS_DIR / (datetime.now().strftime("%Y-%m-%d") + "_logs_py.txt")
CONFIG_PATH = PROJECT_ROOT / "config" / "config.ini"
#
# obtenirTextNivell() -> Funció que serveix per classificar 
#                        el log segons el seu valor númeric
#
# Parametres:
#
# nivell = Tipus d'etiqueta assignat al log en format int.
#          El tornem en format 'str' perquè el format de la
#          etiqueta sigui compatible amb el log.
def obtenir_text_nivell(nivell: int) -> str:
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
    
    # Si la etiqueta està dintre del rang de la taula, 
    # retorna tant la 'key' associat al seu 'value'.
    # Si el número NO està dintre del array associatiu, retorna '[UNKNOWN]'.
    return nivells.get(nivell, '[UNKNOWN]')

#
# obtenir_nivell_log_des_de_ini() -> Funció que serveix per classificar el log segons el seu
#                                    valor númeric especificat al invocador 'obtenirTextNivell()'
def obtenir_nivell_log_des_de_ini(config_path=CONFIG_PATH) -> int:
    
    """
    Llegeix el paràmetre 'log_level_py' de la secció [log] del fitxer config.ini
    Retorna el valor com a enter, o llança excepcions detallades si hi ha errors.
    """

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
    
    # print(valor)

    try:
        # Intentem convertir el valor a enter. Si no és possible, llancem un error
        return int(valor)
    except ValueError:
        raise Exception("❌📄 ERROR! El paràmetre 'log_level_py' no és un enter vàlid")


# log(msg, nivell) -> Escriu una entrada de log si el nivell és prou alt
def log(msg: str, nivell: int = 200):
    try:
        nivell_permes = obtenir_nivell_log_des_de_ini()
    except Exception as e:
        print(e)
        return  # Atura el log si no es pot llegir el fitxer de configuració

    if nivell < nivell_permes:
        return  # El nivell no arriba al mínim requerit
    
    # Per cada log, guarda la data i hora de registre.
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Obtenir el nom net del fitxer que ha cridat el log
    frame = inspect.stack()[1]
    raw_name = os.path.splitext(os.path.basename(frame.filename))[0]
    caller_name = re.sub(r'^\d+_', '', raw_name)  # Elimina prefixos com 9_ o 12_

    # Si el fitxer no existeix, crea'l i afegeix la capçalera avisant que el fitxer es nou
    if not os.path.exists(LOG_FILE):
        # Crea la carpeta si no existeix. Tot i així, aquesta línea de codi no es necessaria
        # ja que PHP ja s'encarrega abans de comprobar si la carpeta 'logs' existeix.
        os.makedirs(LOGS_DIR, exist_ok=True)  
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{caller_name}] ✅📝 S'ha creat un nou fitxer de log anomenat: {LOG_FILE} .\n")
    
    # Format complet del missatge de log
    etiqueta = obtenir_text_nivell(nivell)
    full_msg = f"[{timestamp}] [{caller_name}] {etiqueta} {msg}"
    #
    # Afegim el log
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")

"""

  registrarLog() -> Funció que serveix per gravar cada un dels logs 
                    que genera el nostre projecte.
                    Si no especifiquem el valor númeric del log,
                    s'oferirà el valor per defecte '100' (DEBUG)
 Parametres:
   $missatge = Missatge especificat al invocador 'registarLog()' per escriureu al log
   $nivell   = Especifiquem quina classificació té el log.

+------------+----------------+------------------------------------------+------------------------------+
| Nivell     | Valor numèric  | Descripció                               | Emoji i motiu               |
+------------+----------------+------------------------------------------+------------------------------+
| DEBUG      | 100            | Informació detallada de depuració        | 🔍 Lupa: s'està investigant |
| INFO       | 200            | Esdeveniments informatius (estat normal) | ℹ️ Informació estàndard     |
| NOTICE     | 250            | Esdeveniments normals però rellevants    | ✅ Tot correcte i notable   |
| WARNING    | 300            | Alguna cosa no ideal, però no crítica    | ⚠️ Precaució, pot empitjorar|
| ERROR      | 400            | Errors que impedeixen una acció          | ❌ Alguna cosa ha fallat     |
| CRITICAL   | 500            | Problema greu, cal atenció immediata     | 🛑 Alguna cosa crítica ha fallat    |

| ALERT      | 550            | S'ha de resoldre immediatament           | 🚨 Alarma, acció urgent     |
| EMERGENCY  | 600            | El sistema és inutilitzable              | ☠️ Perill extrem, tot cau   |
+------------+----------------+------------------------------------------+------------------------------+


"""