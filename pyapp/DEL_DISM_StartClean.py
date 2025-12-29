import ctypes
import subprocess
from modules.LogRegister import log


# PowerShell -> Dism.exe /Online /Cleanup-Image /StartComponentCleanup

"""
TOT EL CONTINGUT D'AQUEST SCRIPT ESTA FET AMB IA. EN LA SEGUENT ENTREGA ES SUBSTITUIRA PER CODI HUMÀ.
"""
def is_admin() -> bool:
    """Retorna True si el procés s'està executant amb privilegis d'administrador."""
    try:
        admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        log(f"Comprovació permisos admin: {'SI' if admin else 'NO'}", 200 if admin else 300)
        return admin
    except Exception as e:
        log(f"No s'ha pogut comprovar admin amb IsUserAnAdmin(): {repr(e)}", 400)
        return False


def run_powershell(ps_command: str) -> subprocess.CompletedProcess:
    """
    Executa una comanda mitjançant PowerShell.
    No s'analitza la sortida perquè DISM /StartComponentCleanup
    no retorna informació rellevant per processar.
    """
    log(f"Executant PowerShell: {ps_command}", 100)

    res = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-Command", ps_command
        ],
        shell=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if res.returncode == 0:
        log("StartComponentCleanup executat correctament.", 250)
    else:
        log(f"Error executant StartComponentCleanup (returncode={res.returncode}).", 400)

    return res


def start_component_cleanup() -> bool:
    """
    Executa la neteja del magatzem de components WinSxS amb DISM.
    Aquesta operació és segura i no retorna output rellevant.
    """
    log("Iniciant neteja WinSxS (DISM /StartComponentCleanup)...", 200)

    if not is_admin():
        log("S'atura: cal executar com Administrador per netejar WinSxS.", 400)
        return False

    ps_cmd = "Dism.exe /Online /Cleanup-Image /StartComponentCleanup"
    res = run_powershell(ps_cmd)

    if res.returncode != 0:
        log("La neteja WinSxS no ha finalitzat correctament.", 400)
        return False

    log("Neteja WinSxS finalitzada correctament.", 250)
    return True


if __name__ == "__main__":
    start_component_cleanup()
