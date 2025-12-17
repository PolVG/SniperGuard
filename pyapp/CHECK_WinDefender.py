import subprocess
import json

def is_windows_defender_active():
    '''
    Comanda feta per IA : ps_cmd per comprovar si Windows Defender està actiu.

    PowerShell per obtenir l'estat de Windows Defender:
    Get-MpComputerStatus està disponible a Windows amb Defender
    RealTimeProtectionEnabled indica si la protecció en temps real està activada.
    '''

  
    ps_cmd = r"powershell -NoProfile -Command ""Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled, AntivirusEnabled, AMServiceEnabled | ConvertTo-Json"""

    try:
        #Parametres funcionament: ps_cmd, capture_output per capturar en comptes de escriure, text per obtenir string, check per llançar excepció en error i shell per executar en shell
        result = subprocess.run(ps_cmd, capture_output=True, text=True, shell=True, check=True)
        status = json.loads(result.stdout)

        #Crear diccionari amb els valors d'interès
        return {
            "RealTimeProtectionEnabled": status.get("RealTimeProtectionEnabled"),
            "AntivirusEnabled": status.get("AntivirusEnabled"),
            "AMServiceEnabled": status.get("AMServiceEnabled"),
        }
    
    except Exception as e:
        print(f"Error executant PowerShell per comprovar Windows Defender: {e}")
        #Format diccionari buit en cas d'error perque .get() no falli
        return {}
       


# Evitar que s'executi en ser importat, només quan s'executa directament
if __name__ == "__main__":
    info = is_windows_defender_active()
    print(info)
    # Es fa comparació explícita amb True/False per evitar problemes amb valors None
    if info.get("RealTimeProtectionEnabled") is True:
        print("Windows Defender està activat.")
    elif info.get("RealTimeProtectionEnabled") is False:
        print("Windows Defender no està activat.")
    else:
        print("No es pot determinar l'estat de Windows Defender.")