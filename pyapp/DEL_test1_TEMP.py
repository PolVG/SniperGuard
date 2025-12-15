import subprocess
import ctypes
import time
import os
import shutil

from modules.LogRegister import log

DOWNLOAD_DIR = r"C:\Windows\SoftwareDistribution\Download"


def is_admin() -> bool:
    try:
        admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        log(f"Comprovació permisos admin: {'SI' if admin else 'NO'}", 200 if admin else 300)
        return admin
    except Exception as e:
        log(f"No s'ha pogut comprovar admin amb IsUserAnAdmin(): {repr(e)}", 400)
        return False


def run_cmd(cmd: str) -> subprocess.CompletedProcess:
    log(f"Executant cmd: {cmd}", 100)
    res = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    # Logs de resultat (resum)
    if res.returncode == 0:
        log(f"Cmd OK (returncode=0): {cmd}", 200)
    else:
        log(f"Cmd ERROR (returncode={res.returncode}): {cmd}", 400)

    if res.stdout and res.stdout.strip():
        log(f"STDOUT cmd: {res.stdout.strip()}", 100)

    if res.stderr and res.stderr.strip():
        log(f"STDERR cmd: {res.stderr.strip()}", 300)

    return res


def stop_wuauserv():
    log("Aturant servei wuauserv...", 200)
    print("[INFO] Aturant servei wuauserv…")

    res = run_cmd("sc stop wuauserv")
    if res.stderr and res.stderr.strip():
        print("[WARN] sc stop stderr:", res.stderr.strip())

    # temps perquè Windows alliberi locks
    log("Esperant 3 segons per alliberar locks de Windows Update...", 100)
    time.sleep(3)


def start_wuauserv():
    log("Arrencant servei wuauserv...", 200)
    print("[INFO] Arrencant servei wuauserv…")

    res = run_cmd("sc start wuauserv")
    if res.stderr and res.stderr.strip():
        print("[WARN] sc start stderr:", res.stderr.strip())


def delete_download_contents_cmd():
    log(f"Inici neteja SoftwareDistribution\\Download (cmd). Ruta={DOWNLOAD_DIR}", 200)
    print("[INFO] Esborrant contingut de SoftwareDistribution\\Download (sense eliminar la carpeta)…")

    if not os.path.isdir(DOWNLOAD_DIR):
        log(f"[SKIP] La carpeta no existeix: {DOWNLOAD_DIR}", 300)
        print(f"[WARN] La carpeta no existeix: {DOWNLOAD_DIR}")
        return

    # 1) Esborrar fitxers
    log("Esborrant fitxers amb del /f /q /s ...", 100)
    res = run_cmd(f'del /f /q /s "{DOWNLOAD_DIR}\\*"')
    if res.stderr and res.stderr.strip():
        print("[WARN] del stderr:", res.stderr.strip())

    # 2) Esborrar subcarpetes (NO la carpeta Download)
    # IMPORTANT: en cmd des de Python cal %%D
    log("Esborrant subcarpetes amb rd /s /q ...", 100)
    res = run_cmd(f'for /d %%D in ("{DOWNLOAD_DIR}\\*") do rd /s /q "%%D"')
    if res.stderr and res.stderr.strip():
        print("[WARN] rd stderr:", res.stderr.strip())

    log("Fi neteja SoftwareDistribution\\Download", 250)


def clean_temp_folder(path: str) -> tuple[int, int]:
    """Esborra el contingut d'una carpeta (fitxers + subcarpetes). Retorna (esborrats, errors)."""
    deleted = 0
    errors = 0

    if not path:
        log("clean_temp_folder(): path buit o None", 300)
        return deleted, errors

    if not os.path.exists(path):
        log(f"clean_temp_folder(): path no existeix: {path}", 300)
        return deleted, errors

    log(f"Inici neteja carpeta: {path}", 200)

    try:
        items = os.listdir(path)
    except Exception as e:
        log(f"No s'ha pogut listar contingut de {path}: {repr(e)}", 400)
        return deleted, errors

    for item in items:
        full_path = os.path.join(path, item)
        try:
            if os.path.isfile(full_path) or os.path.islink(full_path):
                os.unlink(full_path)
                deleted += 1
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path, ignore_errors=False)
                deleted += 1
        except Exception as e:
            errors += 1
            # Error puntual: no atura execució
            log(f"No s'ha pogut esborrar: {full_path} ({repr(e)})", 300)

    log(f"Fi neteja carpeta: {path} | esborrats={deleted} | errors={errors}", 250)
    return deleted, errors


def main():
    log("==== Inici neteja TEMP + SoftwareDistribution\\Download ====", 200)
    print("===== NETEJA TEMP + SOFTWAREDISTRIBUTION\\DOWNLOAD =====")

    # TEMP usuari
    total_deleted = 0
    total_errors = 0

    user_temp = os.environ.get("TEMP")
    log(f"Ruta TEMP usuari: {user_temp}", 100)
    d, e = clean_temp_folder(user_temp)
    print(f"[%TEMP%] Esborrats: {d}, Errors: {e}")
    total_deleted += d
    total_errors += e

    # TEMP sistema (pot requerir admin per esborrar-ho tot)
    system_temp = r"C:\Windows\Temp"
    log(f"Ruta TEMP sistema: {system_temp}", 100)
    d, e = clean_temp_folder(system_temp)
    print(f"[C:\\Windows\\Temp] Esborrats: {d}, Errors: {e}")
    total_deleted += d
    total_errors += e

    # SoftwareDistribution\Download (requereix admin)
    if not is_admin():
        log("No s'executa com admin: es salta neteja SoftwareDistribution\\Download", 300)
        print("[WARN] No estàs com Administrador: NO es netejarà SoftwareDistribution\\Download.")
    else:
        log("Execució com admin: s'inicia neteja SoftwareDistribution\\Download", 250)
        print("[INFO] Execució com Administrador: SÍ")
        stop_wuauserv()
        delete_download_contents_cmd()
        start_wuauserv()

    log(f"Resum TEMP: esborrats={total_deleted} errors={total_errors}", 250)

    print("\n--- RESUM ---")
    print(f"Total esborrats (TEMP): {total_deleted}")
    print(f"Total errors (fitxers en ús/permisos): {total_errors}")
    print("===== PROCÉS FINALITZAT =====")

    log("==== Fi neteja TEMP + SoftwareDistribution\\Download ====", 200)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # cap error ha d'escapar sense log
        log(f"Excepció no controlada a __main__: {repr(e)}", 600)
        raise
