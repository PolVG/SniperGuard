import subprocess
import json
from modules.LogRegister import log
"""
Funció is_windows_defender_active():
    Comprova si Windows Defender està actiu utilitzant PowerShell.
    Retorna:
        True  -> Windows Defender està actiu
        False -> Windows Defender no està actiu
        None  -> no s'ha pogut determinar (error, comandament bloquejat, etc.)
    
"""

def is_windows_defender_active():
    '''
    Comanda feta per IA : ps_cmd per comprovar si Windows Defender està actiu.
    '''

    ps = "Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled | ConvertTo-Json"

    try:
        # check_output executa la comanda i retorna output (si falla, llança excepció)
        out = subprocess.check_output(
        ["powershell", "-Command", ps],
        ).decode().strip()

        status = json.loads(out)

        # Retornem només el valor que necessitem
        return status.get("RealTimeProtectionEnabled")
    
    except Exception as e:
        log(f"Error executant PowerShell per comprovar Windows Defender: {e}")
    return None
       


# Evitar que s'executi directament en ser importat, només quan s'executa directament o sigui cridat dins d'un altre script
if __name__ == "__main__":
    windowsdefender = is_windows_defender_active()
    log({"RealTimeProtectionEnabled": windowsdefender})

    # Comparació explícita amb True/False per evitar problemes amb valors None
    if windowsdefender is True:
        log("Windows Defender està activat.")
    elif windowsdefender is False:
        log("Windows Defender no està activat.")
    else:
        log("No es pot determinar l'estat de Windows Defender.")