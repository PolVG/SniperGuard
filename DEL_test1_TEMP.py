import subprocess
import ctypes
import time
import os
import shutil

DOWNLOAD_DIR = r"C:\Windows\SoftwareDistribution\Download"


def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def run_cmd(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def stop_wuauserv():
    print("[INFO] Aturant servei wuauserv…")
    res = run_cmd("sc stop wuauserv")
    if res.stderr.strip():
        print("[WARN] sc stop stderr:", res.stderr.strip())
    time.sleep(3)  # temps perquè Windows alliberi locks


def start_wuauserv():
    print("[INFO] Arrencant servei wuauserv…")
    res = run_cmd("sc start wuauserv")
    if res.stderr.strip():
        print("[WARN] sc start stderr:", res.stderr.strip())


def delete_download_contents_cmd():
    print("[INFO] Esborrant contingut de SoftwareDistribution\\Download (sense eliminar la carpeta)…")

    if not os.path.isdir(DOWNLOAD_DIR):
        print(f"[WARN] La carpeta no existeix: {DOWNLOAD_DIR}")
        return

    # 1) Esborrar fitxers
    res = run_cmd(f'del /f /q /s "{DOWNLOAD_DIR}\\*"')
    if res.stderr.strip():
        print("[WARN] del stderr:", res.stderr.strip())

    # 2) Esborrar subcarpetes (NO la carpeta Download)
    # IMPORTANT: en cmd des de Python cal %%D
    res = run_cmd(f'for /d %%D in ("{DOWNLOAD_DIR}\\*") do rd /s /q "%%D"')
    if res.stderr.strip():
        print("[WARN] rd stderr:", res.stderr.strip())


def clean_temp_folder(path: str) -> tuple[int, int]:
    """Esborra el contingut d'una carpeta (fitxers + subcarpetes). Retorna (esborrats, errors)."""
    deleted = 0
    errors = 0

    if not path or not os.path.exists(path):
        return deleted, errors

    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        try:
            if os.path.isfile(full_path) or os.path.islink(full_path):
                os.unlink(full_path)
                deleted += 1
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path, ignore_errors=False)
                deleted += 1
        except Exception:
            errors += 1

    return deleted, errors


def main():
    print("===== NETEJA TEMP + SOFTWAREDISTRIBUTION\\DOWNLOAD =====")

    # TEMP usuari
    total_deleted = 0
    total_errors = 0

    user_temp = os.environ.get("TEMP")
    d, e = clean_temp_folder(user_temp)
    print(f"[%TEMP%] Esborrats: {d}, Errors: {e}")
    total_deleted += d
    total_errors += e

    # TEMP sistema (pot requerir admin per esborrar-ho tot)
    system_temp = r"C:\Windows\Temp"
    d, e = clean_temp_folder(system_temp)
    print(f"[C:\\Windows\\Temp] Esborrats: {d}, Errors: {e}")
    total_deleted += d
    total_errors += e

    # SoftwareDistribution\Download (requereix admin)
    if not is_admin():
        print("[WARN] No estàs com Administrador: NO es netejarà SoftwareDistribution\\Download.")
    else:
        print("[INFO] Execució com Administrador: SÍ")
        stop_wuauserv()
        delete_download_contents_cmd()
        start_wuauserv()

    print("\n--- RESUM ---")
    print(f"Total esborrats (TEMP): {total_deleted}")
    print(f"Total errors (fitxers en ús/permisos): {total_errors}")
    print("===== PROCÉS FINALITZAT =====")


if __name__ == "__main__":
    main()
