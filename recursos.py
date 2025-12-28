'''
Aquest programa s'ha fet a partir de l'us de IA es fara manualment a la seguent entrega

'''


from modules.LogRegister import log
import os,sys, ctypes
from rich.console import *
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
    def check_admin_privileges():
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
