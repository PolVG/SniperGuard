import subprocess
from modules.LogRegister import log

"""
    Funció defender_update():
    Aplica l'actualització de Windows Defender utilitzant PowerShell.

    retorna:
        True  -> la comanda d'actualització s'ha executat correctament
        False -> no s'ha pogut executar (error/bloquejat)

"""

def defender_update():

    '''
    Comanda feta per IA : ps (comanda powershell) per aplicar la actualització de Windows Defender.
    '''

    ps = "Update-MpSignature | Out-Null"


    try:
        subprocess.check_output(
            ["powershell", "-Command", ps])
        return True
    except Exception:
        return False
    

if __name__ == "__main__":
    result = defender_update()
    if result:
        log("Windows Defender s'han actualitzat correctament.")
    else:
        log("No s'ha pogut actualitzar Windows Defender.")
