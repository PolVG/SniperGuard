from modules.LogRegister import log

# Llegeix una opció per input i valida que:
#  no sigui buida, sigui un dígit, i el número sigui una opció del menú.
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
