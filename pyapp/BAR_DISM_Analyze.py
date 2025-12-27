import ctypes
import subprocess
from modules.LogRegister import log


# DISM /Online /Cleanup-Image /AnalyzeComponentStore


def is_admin() -> bool:
    """Retorna True si el procés s'està executant amb privilegis d'administrador."""
    try:
        admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        log(f"Comprovació permisos admin: {'SI' if admin else 'NO'}", 200 if admin else 300)
        return admin
    except Exception as e:
        log(f"No s'ha pogut comprovar admin amb IsUserAnAdmin(): {repr(e)}", 400)
        return False


def run_cmd(args: list[str]) -> subprocess.CompletedProcess:
    """
    Executa una comanda i retorna el CompletedProcess.
    Captura stdout/stderr per poder registrar informació útil.
    """
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

    if res.returncode == 0:
        log("Cmd OK (returncode=0).", 200)
    else:
        log(f"Cmd ERROR (returncode={res.returncode}).", 400)

    # DISM acostuma a escriure molta informació a stdout (i algun avís a stderr)
    if res.stdout:
        log("Sortida DISM (stdout) capturada correctament.", 250)
    if res.stderr:
        # No sempre és error; DISM pot escriure avisos aquí
        log("DISM ha retornat missatges a stderr (possibles avisos).", 300)

    return res


def analyze_winsxs_component_store() -> bool:
    """
    Analitza el magatzem de components WinSxS amb DISM.
    Retorna True si s'ha executat correctament (returncode == 0).
    """
    log("Iniciant anàlisi WinSxS (DISM /AnalyzeComponentStore)...", 200)

    if not is_admin():
        log("S'atura: cal executar com Administrador per analitzar amb DISM.", 400)
        return False

    res = run_cmd(["DISM", "/Online", "/Cleanup-Image", "/AnalyzeComponentStore"])

    if res.returncode != 0:
        # Log detall de l'error (sense omplir massa el log)
        err_preview = (res.stderr or res.stdout or "").strip().splitlines()[:10]
        if err_preview:
            log("Detall (primeres línies): " + " | ".join(err_preview), 400)
        log("L'anàlisi WinSxS no ha finalitzat correctament.", 400)
        return False

    # Opcional: guardar un resum de les línies més rellevants si existeixen
    # (Per defecte, DISM ja dona el resum al final; aquí en fem un preview curt)
    out_lines = (res.stdout or "").splitlines()
    interesting = []
    keys = (
        "Windows Explorer Reported Size",
        "Actual Size of Component Store",
        "Shared with Windows",
        "Backups and Disabled Features",
        "Cache and Temporary Data",
        "Number of Reclaimable Packages",
        "Component Store Cleanup Recommended",
        "Date of Last Cleanup",
    )
    for line in out_lines:
        if any(k in line for k in keys):
            interesting.append(line.strip())

    if interesting:
        log("Resum anàlisi WinSxS: " + " || ".join(interesting), 250)
    else:
        log("Anàlisi completada. (No s'ha pogut extreure un resum automàtic de la sortida.)", 250)

    log("Anàlisi WinSxS finalitzada correctament.", 250)
    return True


if __name__ == "__main__":
    analyze_winsxs_component_store()
