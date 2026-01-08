import subprocess
from modules.LogRegister import log


"""
Funció defender_update_available():

    Detecta si hi ha (probablement) una actualització de Defender disponible SENSE instal·lar-la,
    preguntant a Windows Update per les actualitzacions de programari pendents.


    Explicació precisa: Windows no publica una actualització universal 'DefenderUpdateAvailable' 
    sino que forma part de les actualitzacions pendents de Windows Update en general per això no es pot garantir
    que una actualització pendent sigui específicament per a Defender.

    Retorna:
        True  -> hi ha actualitzacions pendents reportades per Windows Update
        False -> no hi ha actualitzacions pendents reportades
        None  -> no s'ha pogut determinar (error/bloquejat)
"""


def defender_update_available():
    '''
    Comanda feta per IA : ps (comanda powershell) per comprovar si Windows Defender alguna actualització està disponible.
    '''

    ps = r"""
    Get-MpComputerStatus | Select-Object AntivirusSignatureLastUpdated, AntivirusSignatureVersion
    """


    try:
        # Explicació dels paràmetres dificls: .decode() per convertir bytes a string, subpross.check_output() per capturar la sortida de la comanda
        # i [powershell, -Command, ps] per executar la comanda ps en powershell
        out = subprocess.check_output(["powershell", "-Command", ps]).decode().strip().lower()
        return out
    except Exception:
        return None
    
# Evitar que s'executi directament en ser importat, només quan s'executa directament o sigui cridat dins d'un altre script
if __name__ == "__main__":
    result = defender_update_available()
    
    if result is None:
        log("No s'ha pogut obtenir l'estat de Windows Defender.",250)
    else:
        log(result,300)