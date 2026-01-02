from modules.LogRegister import log
import os,sys, ctypes
from rich.console import *
from pathlib import Path
import zipfile


# Llegeix una opció per input i valida que:
#  no sigui buida, sigui un dígit, i el número sigui una opció del menú.
# ID 400 logs = ERROR


'''
def check_input_user(prompt: str, valid_options: set[str], log_level_bad: int = 400): 



Aquesta funció demana a l'usuari una entrada i valida que sigui vàlida segons les opcions proporcionades.
Rep com a paràmetres:
- prompt: El missatge que es mostrarà a l'usuari per demanar l'entrada.
- valid_options: Un conjunt d'opcions vàlides (com a cadenes).
- log_level_bad: El nivell de registre per a entrades invàlides (per defecte 400).
Retorna:    L'opció vàlida seleccionada per l'usuari, o None si l'entrada és invàlida.

'''
def check_input_user(prompt: str, valid_options: set[str], log_level_bad: int = 400):
    
  
    choice = input(prompt).strip()

    # Si l'entrada està buida torna al menú principal
    if not choice:
        log("La entrada del usuari es buida. Introdueix una opció vàlida.", log_level_bad) 
        return None

    # Si no es pas un dígit (0-9). Torna al menú principal
    if not choice.isdigit():
        log("La entrada del usuari no es pas un dígit. Introdueix un número.", log_level_bad)
        return None

    # Si no està dins del rang d'opcions
    if choice not in valid_options:
        log(f"Opció invàlida: '{choice}'. Opcions vàlides: {sorted(valid_options)}", log_level_bad)
        return None

    return choice

"""
    def check_admin_privileges(): [AQUESTA FUNCIÓ  ESTA FET AMB IA]
Aquesta funció comprova si l'usuari té privilegis elevats (administrador) en un sistema Windows.
Retorna:    True si l'usuari té privilegis elevats, False en cas contrari.
"""
def check_admin_privileges():

    privilegis_elevats = False

    # Detecta si l'usuari té privilegis elevats
    # detectant si el procés de Python s'executa amb Windows\NT
    if os.name == "nt":
        try:
            privilegis_elevats = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            privilegis_elevats = False

    # Missatge a l'usuari
    if privilegis_elevats:
        log("El programa s'està executant amb privilegis elevats.",250)
    else:
        log("Execució amb privilegis d'usuari normal. Algunes funcionalitats quedaran resitringides",300)

    return privilegis_elevats



'''
def eliminate_logs():
Aquesta funció elimina tots els fitxers de log que es troben a la carpeta LOGS_DIR.
Retorna: True si els logs s'han eliminat correctament, False en cas contrari.
'''
def eliminate_logs():
   
    
    PROJECT_ROOT = Path(__file__).resolve().parent
    LOGS_DIR = PROJECT_ROOT / "logs"
    
    try:
        if not LOGS_DIR.exists(): # .exists() retorna True si la ruta existeix
            log(f"La carpeta de logs no existeix: {LOGS_DIR}", 300)
            return False
        
        deleted_count = 0
        for log_file in LOGS_DIR.glob("*.txt"): # .glob() retorna tots els fitxers amb l'extensió .txt
            try:
                log_file.unlink() # .unlink() elimina el fitxer
                deleted_count += 1
                log(f"Fitxer de log eliminat: {log_file.name}", 100)# .name retorna només el nom del fitxer
            except Exception as e:
                log(f"Error al eliminar {log_file.name}: {e}", 400)
        
        log(f"Total de fitxers de log eliminats: {deleted_count}", 250)
        return True
    
    except Exception as e:
        log(f"Error en eliminate_logs(): {e}", 500)
        return False


'''
def compress_logs():
Aquesta funció comprimeix tots els fitxers de log en un arxiu ZIP amb el nom 'logsfiles.zip'.
Retorna: True si la compressió ha estat exitosa, False en cas contrari.
'''
def compress_logs():

    
    PROJECT_ROOT = Path(__file__).resolve().parent
    LOGS_DIR = PROJECT_ROOT / "logs"
    ZIP_FILE = LOGS_DIR / "logsfiles.zip"
    
    try:
        if not LOGS_DIR.exists():
            log(f"La carpeta de logs no existeix: {LOGS_DIR}", 300)
            return False
        
        # Crear el fitxer ZIP
        with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf: # ZIP_DEFLATED és per la compressió
            log_files = list(LOGS_DIR.glob("*.txt")) # glob() retorna tots els fitxers amb l'extensió .txt
            
            if not log_files:
                log("No hi ha fitxers de log per comprimir.", 300)
                return False
            
            for log_file in log_files:
                # Afegir fitxer al ZIP (només el nom del fitxer, no la ruta completa)
                zipf.write(log_file, arcname=log_file.name) # arcname evita incloure la ruta completa dins del ZIP
                log(f"Fitxer afegit al ZIP: {log_file.name}", 100)
        
        log(f"Arxiu ZIP creat correctament: {ZIP_FILE}", 250)
        print(f"\n✅ Fitxers comprimits a: {ZIP_FILE}\n")
        return True
    
    except Exception as e:
        log(f"Error en compress_logs(): {e}", 500)
        print(f"\n❌ Error comprimint fitxers: {e}\n")
        return False

'''
def decompress_logs():
Aquesta funció busca el primer arxiu ZIP de logs i el descomprimeix a la carpeta de logs.
Retorna: True si la descompressió ha estat exitosa, False en cas contrari.
'''
def decompress_logs():
    

    PROJECT_ROOT = Path(__file__).resolve().parent
    LOGS_DIR = PROJECT_ROOT / "logs"

    try:
        if not LOGS_DIR.exists():
            log(f"La carpeta de logs no existeix: {LOGS_DIR}", 300)
            return False

        zip_files = sorted(LOGS_DIR.glob("*.zip"))
        if not zip_files:
            log("No s'ha trobat cap fitxer ZIP de logs.", 300)
            return False

        target_zip = zip_files[0] # Selecciona el primer fitxer ZIP trobat
        if not zipfile.is_zipfile(target_zip):
            log(f"El fitxer no és un ZIP vàlid: {target_zip}", 400)
            return False

        with zipfile.ZipFile(target_zip, 'r') as zipf:
            zipf.extractall(LOGS_DIR)

        log(f"Arxiu ZIP descomprimit correctament: {target_zip}", 250)
        print(f"\n✅ Fitxers descomprimits des de: {target_zip}\n")
        return True

    except Exception as e:
        log(f"Error en decompress_logs(): {e}", 500)
        print(f"\n❌ Error descomprimint fitxers: {e}\n")
        return False