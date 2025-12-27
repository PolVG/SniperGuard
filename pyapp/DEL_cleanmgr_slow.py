# import ctypes
# import subprocess
# import sys
# from modules.LogRegister import log

# """
# TOT EL CONTINGUT D'AQUEST SCRIPT ESTA FET AMB IA. EN LA SEGUENT ENTREGA ES SUBSTITUIRA PER CODI HUMÀ.
# """
# import ctypes
# import subprocess
# import time
# from modules.LogRegister import log

# PROFILE_ID = 1

# def is_admin() -> bool:
#     try:
#         admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
#         log(f"Comprovació permisos admin: {'SI' if admin else 'NO'}", 200 if admin else 300)
#         return admin
#     except Exception as e:
#         log(f"No s'ha pogut comprovar admin amb IsUserAnAdmin(): {repr(e)}", 400)
#         return False


# def run_cmd(args: list[str]) -> subprocess.CompletedProcess:
#     cmd_str = " ".join(args)
#     log(f"Executant cmd: {cmd_str}", 100)
#     return subprocess.run(
#         args,
#         shell=False,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True,
#         errors="replace",
#     )


# def is_process_running(image_name: str) -> bool:
#     # tasklist retorna la llista de processos; si hi és, vol dir que encara està actiu
#     res = subprocess.run(
#         ["tasklist", "/FI", f"IMAGENAME eq {image_name}"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True,
#         errors="replace",
#         shell=False,
#     )
#     return image_name.lower() in (res.stdout or "").lower()


# def sageset_and_wait(profile_id: int, timeout_sec: int = 600) -> bool:
#     log(f"Obrint cleanmgr /SAGESET:{profile_id} (configuració manual)", 200)

#     # Llença la GUI (no bloquegem amb run, perquè pot retornar abans d'hora)
#     subprocess.Popen(["cleanmgr.exe", f"/SAGESET:{profile_id}"], shell=False)

#     log("Esperant que l'usuari tanqui la finestra de configuració (OK)...", 200)

#     start = time.time()
#     # Espera fins que no hi hagi cap cleanmgr.exe actiu
#     while True:
#         if not is_process_running("cleanmgr.exe"):
#             log("Finestra de configuració tancada. Continuem.", 200)
#             return True

#         if time.time() - start > timeout_sec:
#             log(f"Timeout esperant el tancament de cleanmgr (>{timeout_sec}s).", 400)
#             return False

#         time.sleep(1)


# def sagerun(profile_id: int) -> bool:
#     log(
#         "INFO: Durant la neteja poden aparèixer dues finestres consecutives "
#         "(Scanning -> Cleaning). Això és normal. No tanquis el procés.",
#         300
#     )
#     log(f"Executant cleanmgr /SAGERUN:{profile_id}", 200)
#     res = run_cmd(["cleanmgr.exe", f"/SAGERUN:{profile_id}"])

#     if res.returncode != 0:
#         log(f"SAGERUN ha fallat (returncode={res.returncode}).", 400)
#         if res.stderr and res.stderr.strip():
#             log(f"STDERR: {res.stderr.strip()}", 300)
#         return False

#     log("Neteja automàtica finalitzada correctament.", 250)
#     return True


# def main():
#     if not is_admin():
#         log("AVÍS: no estàs com Admin. Pot faltar 'Clean up system files'.", 300)

#     ok = sageset_and_wait(PROFILE_ID)
#     if not ok:
#         log("No s'ha pogut confirmar el tancament de SAGESET.", 400)
#         return

#     log("Executant SAGERUN automàticament després de SAGESET...", 200)
#     sagerun(PROFILE_ID)

# if __name__ == "__main__":
#     main()
