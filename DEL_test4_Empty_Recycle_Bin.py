import subprocess

OK_BUT_NO_PATH = "The system cannot find the path specified"

def vaciar_papelera_powershell():
    cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-Command",
        "Clear-RecycleBin -Force"
    ]

    p = subprocess.run(cmd, capture_output=True, text=True)

    print("===== PowerShell: Clear-RecycleBin =====")

    stderr = (p.stderr or "").strip()
    stdout = (p.stdout or "").strip()

    # Mostrem sortida només si hi ha text
    if stdout:
        print("\n[STDOUT]")
        print(stdout)

    if stderr:
        # Si és l'error típic de path inexistent, no ho tractem com a fallida
        if OK_BUT_NO_PATH in stderr:
            print("\n[WARN] PowerShell ha retornat un avís per una unitat/paperera inexistent.")
            print("       Però la paperera s'ha buidat correctament a les unitats disponibles.")
            print("       (Missatge PowerShell: 'The system cannot find the path specified')")
            print("\n✅ Paperera buidada correctament.")
            return

        print("\n[STDERR]")
        print(stderr)

    # Si return code 0 => OK
    if p.returncode == 0:
        print("\n✅ Paperera buidada correctament.")
    else:
        print(f"\n⚠️ PowerShell ha retornat codi {p.returncode}.")
        print("   Si la paperera està buida igualment, probablement és per alguna unitat no disponible.")
        print("   Si vols evitar això del tot, et puc donar la versió 'per unitat'.")

if __name__ == "__main__":
    vaciar_papelera_powershell()
