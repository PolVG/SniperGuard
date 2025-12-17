from modules.LogRegister import log
import os,sys, ctypes
# Llegeix una opció per input i valida que:
#  no sigui buida, sigui un dígit, i el número sigui una opció del menú.
# ID 400 logs = ERROR
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
    Comprova si el script s'està executant amb privilegis elevats.
    SniperGuard necessita alerta de quines funcionalitats requerixen
    privilegis d'admin i quines no.
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
        log("Execució amb privilegis d'usuari normal. Algunes funcionalitats quedaran resitringides",400)

    return privilegis_elevats
