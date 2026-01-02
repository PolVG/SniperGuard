import ctypes
import subprocess
from modules.LogRegister import log


# Dism.exe /online /Cleanup-Image /StartComponentCleanup

def is_admin() -> bool:
    """Retorna True si el procés s'està executant amb privilegis d'administrador."""
    try:
        admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        log(f"Comprovació permisos admin: {'SI' if admin else 'NO'}", 200 if admin else 300)
        return admin
    except Exception as e:
        log(f"No s'ha pogut comprovar admin amb IsUserAnAdmin(): {repr(e)}", 400)
        return False

# Executa la comanda amb CMD per iniciar amb cleanmgr.exe
# un procés ràpid de neteja del nostre PC.
# RECORDA! La comanda "cleanmgr.exe /AUTOCLEAN" no retorna output
#          un cop
def run_cmd(args: list[str]) -> subprocess.CompletedProcess:
    cmd_str = " ".join(args)
    log(f"Executant cmd: {cmd_str}", 100)
    res = subprocess.run(
        args,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    
    # Logs de resultat (resum)
    if res.returncode == 0:
        log(f"Cmd OK (returncode=0): {args}", 200)
    else:
        log(f"Cmd ERROR (returncode={res.returncode}): {args}", 400)

    return res


def start_fast_clean() -> bool:
    """
    Llença Disk Cleanup en mode automàtic.
    Retorna True si s'ha executat amb èxit (returncode == 0).
    """
    log("Arrencant neteja ràpida (cleanmgr /AUTOCLEAN)...", 200)

    if not is_admin():
        log("S'atura: cal executar com Administrador per una neteja més completa.", 400)
        return False

    res = run_cmd(["cleanmgr.exe", "/AUTOCLEAN"])

    # No esperis stderr en cleanmgr; normalment no retorna res.
    if res.returncode != 0:
        log("La neteja no ha finalitzat correctament (returncode != 0).", 400)
        return False

    log("Neteja ràpida finalitzada correctament.", 250)
    return True


if __name__ == "__main__":
    start_fast_clean()