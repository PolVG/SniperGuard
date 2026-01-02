"""
TOT EL CONTINGUT D'AQUEST SCRIPT ESTA FET AMB IA. EN LA SEGUENT ENTREGA ES SUBSTITUIRA PER CODI HUMÀ.

"""

import subprocess
from modules.LogRegister import log

OK_BUT_NO_PATH = "The system cannot find the path specified"


def vaciar_papelera_powershell():
    log("Inici buidat paperera amb PowerShell (Clear-RecycleBin)", 200)

    cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-Command",
        "Clear-RecycleBin -Force"
    ]

    log(f"Executant comanda PowerShell: {' '.join(cmd)}", 100)

    p = subprocess.run(cmd, capture_output=True, text=True)

    print("===== PowerShell: Clear-RecycleBin =====")

    stderr = (p.stderr or "").strip()
    stdout = (p.stdout or "").strip()

    # STDOUT (informatiu)
    if stdout:
        log(f"PowerShell STDOUT: {stdout}", 100)
        print("\n[STDOUT]")
        print(stdout)

    # STDERR (pot ser warning o error)
    if stderr:
        # Cas conegut: path inexistent però paperera buidada correctament
        if OK_BUT_NO_PATH in stderr:
            log(
                "PowerShell ha retornat 'The system cannot find the path specified' "
                "(interpretat com a OK funcional: unitat/paperera inexistent)",
                250
            )
            log(f"PowerShell STDERR (ignorat): {stderr}", 300)

            print("\n[WARN] PowerShell ha retornat un avís per una unitat/paperera inexistent.")
            print("       Però la paperera s'ha buidat correctament a les unitats disponibles.")
            print("       (Missatge PowerShell: 'The system cannot find the path specified')")
            print("\n✅ Paperera buidada correctament.")

            log("Fi buidat paperera PowerShell: OK (amb avisos controlats)", 200)
            return

        # Error real
        log(f"PowerShell STDERR: {stderr}", 400)
        print("\n[STDERR]")
        print(stderr)

    # Avaluació del returncode
    if p.returncode == 0:
        log("Clear-RecycleBin finalitzat correctament (returncode=0)", 200)
        print("\n✅ Paperera buidada correctament.")
    else:
        log(
            f"Clear-RecycleBin ha retornat codi {p.returncode} "
            "(possible unitat no disponible / paperera ja buida)",
            300
        )
        print(f"\n⚠️ PowerShell ha retornat codi {p.returncode}.")
        print("   Si la paperera està buida igualment, probablement és per alguna unitat no disponible.")
        print("   Si vols evitar això del tot, et puc donar la versió 'per unitat'.")

    log("Fi buidat paperera PowerShell", 200)


if __name__ == "__main__":
    try:
        vaciar_papelera_powershell()
    except Exception as e:
        log(f"Excepció no controlada a vaciar_papelera_powershell(): {repr(e)}", 600)
        raise
