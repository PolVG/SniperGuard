# llibreries externes
import sys, os
import subprocess
from pathlib import Path
from datetime import datetime

from rich import *
from rich.console import *
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
import time 


# llibreries internes
from modules.LogRegister import log, init_log_file, get_current_log_file, manage_logs, print_log_levels_table, check_current_log_level
import recursos
from recursos import check_input_user, check_admin_privileges, erase_logs, compress_logs, decompress_logs


# Configuració global
console = Console()
table = Table(show_lines=True,border_style="yellow")

# Definició de rutes globals
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR

PYAPP_DIR = PROJECT_ROOT / "pyapp"
LOGS_DIR = PROJECT_ROOT / "logs"
MODULES_DIR = PROJECT_ROOT / "modules"

# Cada dia, es crea un nou fitxer de log.
LOG_FILE = LOGS_DIR / (datetime.now().strftime("%Y-%m-%d") + "_logs_py.txt")

MODE_BAR = 1  # identificar
MODE_DEL = 2  # identificar + esborrar


'''
def show_log_link():
Aquesta funció mostra a la consola un enllaç clicable al fitxer de log actual.
Aquesta funció utilitza URI per permetre als usuaris obrir el fitxer directament des de la consola.

'''
def show_log_link():
    
    log_file = get_current_log_file() # Obtenir la ruta del fitxer de log actual
    
    if log_file and log_file.exists():
        log_path_str = str(log_file.resolve()) # str = convertir a string per poder manipular la ruta i .resolve() per obtenir la ruta absoluta
        log_uri = f"file:///{log_path_str.replace(chr(92), '/')}"# Convertir a URI i substituir '\' per '/' , chr(92) és '\'
        
        print("\n")
        panel = Panel(
            f"[bold cyan]📁 Ruta del log:[/bold cyan]\n\n"
            f"[link={log_uri}]{log_path_str}[/link]\n\n"
            f"[white]Clica l'enllaç per obrir el fitxer[/white]", 
            title="[bold green]✅ Execució finalitzada[/bold green]",
            border_style="green",
            padding=(1, 2)
        )
        console.print(panel)
        print("\n")
    else:
        console.print("[yellow]⚠️ No s'ha pogut trobar el fitxer de log.[/yellow]")

    
'''
def run_script(script_name: str):
Aquesta funció s'utilitza per executar un script Python específic des de la ubicació PYAPP_DIR.
Rep com a paràmetre el nom de l'script i gestiona la seva execució, capturant la sortida i els errors.
'''
def run_script(script_name:  str):
    
    script_path = PYAPP_DIR / script_name

    if not script_path.exists():
        log(f"No existeix el fitxer: {script_path}", 400)
        console.print(f"[bold red]❌ No s'ha trobat:  {script_name}[/bold red]")
        return

    if not sys.executable: #ruta de l'intèrpret de Python
        log("sys.executable no està disponible.", 400)
        return

    log(f"Preparant execució de script: {script_path}", 200)

    try:
        #!!! Les variables env, system_encoding i process s'han fet amb ajuda de la IA !!!!
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT)

        current_log = get_current_log_file()
        if current_log is None:
            current_log = init_log_file()
        env["SNIPERGUARD_LOG_FILE"] = str(current_log)
        
        system_encoding = sys.stdout.encoding or 'utf-8' # Obtenir l'encoding del sistema, per defecte 'utf-8' si no està definit

        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            env=env,
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess. PIPE,
            text=True,
            encoding=system_encoding,
            errors='replace'  # Per evitar errors d'encoding
        )
        

       #PROGRÉS AMB SPINNER ANIMAT

        with Progress(
            SpinnerColumn(), #Spinner animat, simplement estetic
            TextColumn("[bold cyan]{task.description}"), #TextColumn per mostrar el text de la tasca
            TimeElapsedColumn(), #Mostra el temps transcorregut
            console=console, # Pàrametre obligatori per especificar la consola on es mostrarà el progrés
            transient=True  # Desapareix quan acaba
        ) as progress:
            
            task = progress.add_task(f"Executant {script_name}.. .", total=None)
            
            # Mentre el procés està actiu, actualitzar el spinner
            while process.poll() is None:  # poll() retorna None mentre s'executa
                time.sleep(0.1)  # Comprovar cada 0.1 segons
        
      
        stdout, stderr = process.communicate(timeout=200) # Espera que el procés acabi, amb timeout de 200 segons i captura stdout i stderr
        
       
        if process.returncode == 0: # Si el procés ha acabat correctament
            log(f"Script {script_name} finalitzat OK", 250)
            console.print(f"[bold green] {script_name} completat amb èxit[/bold green]")
        else:
            log(f"Script {script_name} returncode={process.returncode}", 300)
          
        if stdout and stdout.strip(): # Si hi ha sortida estàndard no buida
     
            log(f"STDOUT {script_name}: {stdout.strip()}", 250)

        if stderr and stderr.strip(): # Si hi ha sortida d'error no buida
            log(f"STDERR {script_name}:  {stderr.strip()}", 400)

    except subprocess.TimeoutExpired: # excepte si el procés es triga massa, el timeout s'ha definit a process.communicate() = 200 segons
        log(f"Timeout executant {script_name}", 400)
        console.print("[bold red]❌ Timeout: procés massa lent[/bold red]")
        process.kill()

    except Exception as e:
        log(f"Error executant {script_name}: {e}", 400)
        console.print(f"[bold red]❌ Error: {e}[/bold red]")

'''
def run_cleaning_from_gui(mode_choice: str, cleaning_choice: str):
Aquesta funció s'utilitza per executar les operacions de neteja des de la interfície gràfica d'usuari (GUI).
Rep com a paràmetres les opcions seleccionades per l'usuari a la GUI i executa l'script corresponent segons aquestes opcions.
'''
def run_cleaning_from_gui(mode_choice: str, cleaning_choice: str):
    log("Executant run_cleaning_from_gui() des de GUI", 200)

    if not check_admin_privileges():
        print("ERROR! Aturant el programa.")
        print("SniperGuard requereix ser executat com administrador per funcionar.")
        print("Si ets administrador, clica amb el botó dret sobre la icona de SniperGuard")
        print("i selecciona: 'Executa com a administrador'")
        log("SniperGuard s'ha aturat al no arrencar-se com administrador.",250)
        sys.exit()

    # Si el programa s'ha arrencat correctament, 
    # executem SniperGuard com a administrador.    
    log("SniperGuard s'ha executat correctament amb privilegis administratius.",250)
       
    if mode_choice not in {"1", "2"}:
        log(f"Mode invàlid rebut des de GUI: {mode_choice}", 400)
        return

    mode = MODE_BAR if mode_choice == "1" else MODE_DEL

    bar_options = {
        "1": ("Estat arxius temporals", "BAR_test1_TEMP.py"),
        "2": ("Estat navegadors (historial/cookies/caché)", "BAR_test12_Full_Clean_browser.py"),
        "3": ("Estat paperera de reciclatge", "BAR_test4_Empty_Recycle_Bin.py"),
    }

    del_options = {
        "1": ("Netejar arxius temporals", "DEL_test1_TEMP.py"),
        "2": ("Netejar navegadors (historial/cookies/caché)", "DEL_test12_Full_Clean_browser.py"),
        "3": ("Buidar paperera de reciclatge", "DEL_test4_Empty_Recycle_Bin.py"),
    }

    options = bar_options if mode == MODE_BAR else del_options

    if cleaning_choice not in options:
        log(f"Opció cleaning invàlida rebuda des de GUI: {cleaning_choice}", 400)
        return

    label, script = options[cleaning_choice]
    log(f"Executant acció (GUI): {label}", 200)
    run_script(script)


'''
def cleaning_menu(mode):
Aquesta funció mostra un menú de neteja a l'usuari i executa l'script corresponent segons la seva elecció.
'''
def cleaning_menu(mode):
    log("Mostrant al usuari les opcions disponibles de neteja.", 100)
    recursos.play_sound("reloading.wav")
    BAR_OPTIONS = {
        "1": ("Estat arxius temporals", "BAR_test1_TEMP.py"),
        "2": ("Estat navegadors (historial/cookies/caché)", "BAR_test12_Full_Clean_browser.py"),
        "3": ("Estat paperera de reciclatge", "BAR_test4_Empty_Recycle_Bin.py"),
        "4": ("Estat carpeta 'C:\\Windows\\WinSxS' (+3 min)", "BAR_DISM_Analyze.py"),
        "5": ("Tornar al menú", None),
    }

    DEL_OPTIONS = {
        "1": ("Netejar arxius temporals", "DEL_test1_TEMP.py"),
        "2": ("Netejar navegadors (historial/cookies/caché)", "DEL_test12_Full_Clean_browser.py"),
        "3": ("Buidar paperera de reciclatge", "DEL_test4_Empty_Recycle_Bin.py"),
        "4": ("Realitzar una neteja ràpida amb 'cleanmgr.exe'", "DEL_cleanmgr_fast.py"),
        "5": ("Realitzar una neteja lenta amb 'cleanmgr.exe'", "DEL_cleanmgr_slow.py"),
        "6": ("Esborrar arxius residuals a 'C:\\Windows\\WinSxS'", "DEL_DISM_StartClean.py"),
        "7": ("Tornar al menú", None),
    }

    if mode == MODE_BAR:
        log("Mode BAR actiu: mostrant opcions de comprovació", 200)
        options = BAR_OPTIONS
    else:
        log("Mode DEL actiu: mostrant opcions de neteja", 200)
        options = DEL_OPTIONS


    print("\n")
    panel = Panel(
        Align.center("[bold green] Opcions de Cleaning [/bold green]", vertical="middle"),
        border_style="green",
        style="on grey15",
        padding=(1, 6),
    )
    console.print(panel)
    print("\n")

    table = Table(
        show_lines=True,           
        header_style="bold light_green",
        padding=(0, 1),
    )

    table.add_column("ID", justify="center", style="bold green", no_wrap=True, width=4)
    table.add_column("Opció", justify="center", style="bold green")
    
    for key, (label, _) in options.items(): # _ per ignorar el segon valor 
        table.add_row(key, label)
    console.print(table)
    print("\n")
    

    choice = check_input_user("Introdueix una opció: ", set(options.keys())) # set() per convertir les claus en conjunt set
    
    # Només volem que es mostri aquest missatge si l'usuari
    # realitza una neteja exhaustiva.
    if mode != MODE_BAR and choice == "5":
        console.print("[bold yellow]Per fer una neteja exhaustiva, seleciona primer de cleanmgr.exe quins elements vol eliminiar. Després, prem 'OK' [bold yellow]")
        console.print("[yellow underline]Obrint 'cleanmgr.exe'. Si us plau esperi... [yellow underline]")
    
    if choice is None:
        recursos.play_sound("shell.wav")
        log("Sortint de la funció cleaning_menu()", 100)
        return

    log(f"L'usuari ha triat opció cleaning_menu: '{choice}' (mode={mode})", 200)

    label, script = options[choice]

    if script is None:
        recursos.play_sound("shell.wav")
        log("Usuari torna al menú anterior", 250)
        return
    recursos.play_sound("gun.wav")
    log(f"Executant acció: {label}", 200)
    run_script(script)


'''
def hardening_menu(mode):
Aquesta funció mostra un menú de hardening a l'usuari i executa l'script corresponent segons la seva elecció.
'''
def hardening_menu(mode):
    log("Mostrant al usuari les opcions disponibles de hardening.", 100)
    
    recursos.play_sound("reloading.wav")
    BAR_OPTIONS = {
        "1": ("Comprovar si Windows Defender està actiu", "HARD_WinDefender.py"),
        "2": ("Comprovar si falten actualitzacions a Windows Defender", "HARD_WinDefenderUpdateAvailable.py"),
        "3": ("Comprovar si falten actualitzacions a Windows Update", "BAR_test5_UPDATE.py"),
        "4": ("Tornar al menú", None),
    }

    DEL_OPTIONS = {
        "1": ("Actualitzar Windows Defender (-30 sec)", "HARD_WinDefenderUpdate.py"),
        "2": ("Actualitzar Windows amb Windows Update (+10 min)", "HARD_WindowsUpdate.py"),
        "3": ("Tornar al menú", None),
    }

    if mode == MODE_BAR:
        log("Mode BAR actiu: mostrant opcions de comprovació", 200)
        options = BAR_OPTIONS
    else:
        log("Mode DEL actiu: mostrant opcions de neteja", 200)
        options = DEL_OPTIONS
    
    print("\n")
    panel = Panel(
        Align.center("[bold yellow] Opcions de Bastionatge [/bold yellow]", vertical="middle"),
        border_style="yellow",
        style="on grey15",
        padding=(1, 6),
    )
    console.print(panel)
    print("\n")

    table = Table(
        show_lines=True,           
        header_style="bold yellow",
        padding=(0, 1),
    )
    table.add_column("ID", justify="center", style="bold bright_white", no_wrap=True, width=4)
    table.add_column("Opció", justify="center", style="bold yellow")
    for key, (label, _) in options.items():
        table.add_row(key, label)
    console.print(table)
    print("\n")

    choice = check_input_user("Introdueix una opció: ", set(options.keys()))
    if choice is None:

        log("Sortint de la funció hardening_menu()", 100)
        return

    log(f"L'usuari ha triat opció hardening_menu: '{choice}' (mode={mode})", 200)

    label, script = options[choice]

    if script is None:
        recursos.play_sound("shell.wav")
        log("Usuari torna al menú anterior", 250)
        return
    recursos.play_sound("gun.wav")
    log(f"Executant acció: {label}", 200)
    run_script(script)


'''
def sons_FX(): 
Aquesta funció permet a l'usuari activar o desactivar els efectes de so (FX) dins de SniperGuard.

'''
def sons_FX():
    global SOUND_ENABLED # Per modificar la variable global
    while True:
        print("\n")
        panel = Panel(
            Align.center("[bold orange3 underline] Sons FX [/bold orange3 underline]", vertical="middle"),
            border_style="orange3",
            style="on grey15",
            padding=(1, 6),
        )
        console.print(panel)
        print("\n")
        console.print("Què vols fer?", style="bold white underline")
        table = Table(show_lines=True,border_style="orange3")
        table.add_column("ID", justify="center", header_style="bold white", style="bold cyan", no_wrap=True)
        table.add_column("Títol", justify="center", header_style="bold white", style="bold white")
        table.add_column("Descripció", justify="center",header_style="bold white", style="bold white")

        table.add_row("1.", "Activar FX", "Es reprodueixen arxius de so mentre s'utilitza SniperGuard.")
        table.add_row("2.", "Desactivar FX", "SniperGuard silenciós.")
        table.add_row("3.", "Sortir", "Torna al menú principal.")
        console.print(table)

        try:
            choice = check_input_user("Introdueix una opció: ", {"1", "2", "3"})
        except Exception as e:
            log(f"Error en check_input_user() dins choose_mode(): {e}", 400)
            choice = None

        if choice == "1":
            log("Usuari ha seleccionat SONS FX", 250)
            recursos.SOUND_ENABLED = True
            recursos.play_sound("reloading.wav")
            return
        elif choice == "2":
            log("Usuari ha seleccionat DESACTIVAR FX", 250)
            recursos.SOUND_ENABLED = False
            return
        else:
            recursos.play_sound("shell.wav")
            log("Usuari ha seleccionat tornar al menú principal", 250)
            return None

'''
def choose_logs():
Aquesta funció permet a l'usuari gestionar els logs de SniperGuard, oferint opcions per comprimir, descomprimir, esborrar i configurar el baròmetre de logs.

'''
def choose_logs():
    
    while True:
        print("\n")
        panel = Panel(
            Align.center("[bold sky_blue1 underline] Gestió de logs [/bold sky_blue1 underline]", vertical="middle"),
            border_style="sky_blue1",
            style="on grey15",
            padding=(1, 6),
        )
        console.print(panel)
        print("\n")
        console.print("Què vols fer?", style="bold white underline")
        table = Table(show_lines=True,border_style="sky_blue1")
        table.add_column("ID", justify="center", header_style="bold white", style="bold cyan", no_wrap=True)
        table.add_column("Títol", justify="center", header_style="bold white", style="bold white")
        table.add_column("Descripció", justify="center",header_style="bold white", style="bold white")

        table.add_row("1.", "Comprimir (ZIP)", "Comprimeix els logs en un .ZIP")
        table.add_row("2.", "Descomprimir (UNZIP)", "Descomprimeix els logs d'un .ZIP")
        table.add_row("3.", "Esborrar logs", "Esborra tots els logs de SpineGuard.")
        table.add_row("4.", "Baròmetre logs", "Defineix quina categoria de logs a mostrar.")
        table.add_row("5.", "Sortir", "Tornar al menú principal")
        console.print(table)

        try:
            choice = check_input_user("Introdueix una opció: ", {"1", "2", "3","4","5","6","7"})
        except Exception as e:
            log(f"Error en check_input_user() dins choose_mode(): {e}", 400)
            choice = None

        if choice == "1":
            log("Usuari ha seleccionat COMPRIMIR", 250)
            compress_logs()
            return None
        elif choice == "2":
            log("Usuari ha seleccionat DESCOMPRIMIR", 250)
            decompress_logs()
            return None
        elif choice == "3":
            log("Usuari ha seleccionat ESBORRAR LOGS", 250)           
            #
            erase_logs()
            #
            console.print("[bold green] Els logs s'han esborrat correctament. [bold green]")
            console.print("[bold green] Es veu un nou fitxer de logs degut a que SniperGuard torna a arrencar. [bold green]")
            return None
        
        elif choice == "4":
            log("Usuari ha seleccionat BARÒMETRE LOGS", 250)
            #
         
            print_log_levels_table()
            current_log = check_current_log_level()
            print()
            console.print(f"Nivell de log actual: {current_log}")
            print()
            console.print(f"Prem '1' per tornar al menú principal")
            print()
            new_log = check_input_user("Introdueix el nivell de log a guardar: ", {"1", "100", "200", "250","300","400"})
            
            if new_log == '1':
                console.print(f"[bold yellow]Retornant al menú principal.[bold yellow]")
                return None
            else:
                manage_logs(current_log, new_log)
                return None
        else:
            recursos.play_sound("shell.wav")
            log("Usuari ha seleccionat tornar al menú principal", 250)
            return None
        
'''
def choose_mode():
Aquesta funció demana a l'usuari que triï entre dos modes: BAR (només comprovar) o DEL (comprovar + esborrar).
'''
def choose_mode():

    while True:
        print("\n")
        panel = Panel(
            Align.center("[bold green underline] CLEANING (Neteja) [/bold green underline]", vertical="middle"),
            border_style="green",
            style="on grey15",
            padding=(1, 6),
        )
        console.print(panel)
        print("\n")
        console.print("Què vols fer?", style="bold white underline")
        table = Table(show_lines=True,border_style="green")
        table.add_column("ID", justify="center", header_style="bold white", style="bold cyan", no_wrap=True)
        table.add_column("Títol", justify="center", header_style="bold white", style="bold white")
        table.add_column("Descripció", justify="center",header_style="bold white", style="bold white")

        table.add_row("1.", "Identificar estat (BAR)", "Només comprovar")
        table.add_row("2.", "Identificar cleaning (DEL)", "comprovar + netejar")
        table.add_row("3.", "Sortir", "Tornar al menú principal")
        console.print(table)

        try:
            choice = check_input_user("Introdueix una opció: ", {"1", "2", "3","4","5","6","7"})
        except Exception as e:
            log(f"Error en check_input_user() dins choose_mode(): {e}", 400)
            choice = None

        if choice == "1":
            log("Usuari ha seleccionat mode BAR", 250)
            return MODE_BAR
        elif choice == "2":
            log("Usuari ha seleccionat mode DEL", 250)
            return MODE_DEL
        else:
            recursos.play_sound("shell.wav")
            log("Usuari ha seleccionat tornar al menú principal", 250)
            return None

'''
def choose_hardening_mode():
Aquesta funció demana a l'usuari que triï entre dos modes de hardening: BAR (només comprovar) o HARD (comprovar + hardening).
'''
def choose_hardening_mode():

    while True:
        print("\n")
        panel = Panel(
            Align.center("[bold yellow underline] HARDENING (Bastionatge) [/bold yellow underline]", vertical="middle"),
            border_style="yellow",
            style="on grey15",
            padding=(1, 6),
        )
        console.print(panel)
        print("\n")
        console.print("Què vols fer?", style="bold white underline")
        table = Table(show_lines=True,border_style="yellow")
        table.add_column("ID", justify="center", header_style="bold white", style="bold cyan", no_wrap=True)
        table.add_column("Títol", justify="center", header_style="bold white", style="bold yellow")
        table.add_column("Descripció", justify="center",header_style="bold white", style="bold yellow")

        table.add_row("1.", "Identificar estat (BAR)", "Només comprovar")
        table.add_row("2.", "Identificar hardening (HARD)", "comprovar + hardening")
        table.add_row("3.", "Sortir", "Tornar al menú principal")
        console.print(table)
        try:
            choice = check_input_user("Introdueix una opció: ", {"1", "2", "3"})
        except Exception as e:
            log(f"Error en check_input_user() dins choose_hardening_mode(): {e}", 400)
            choice = None

        if choice == "1":
            log("Usuari ha seleccionat mode BAR", 250)
            return MODE_BAR
        elif choice == "2":
            log("Usuari ha seleccionat mode DEL", 250)
            return MODE_DEL
        else:
            recursos.play_sound("shell.wav")
            log("Usuari ha seleccionat tornar al menú principal", 250)
            return None


'''
def print_banner():
Aquesta funció imprimeix un banner inicial de SniperGuard a la consola.
'''
def print_banner():
    print("\n")
    console.rule("")
    log("Executant la funció 'print_banner()' per mostrar el banner inicial.", 100)
    print("\n")
    console.print("                  ███████╗███╗   ██╗██╗██████╗ ███████╗██████╗  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗", justify="center", style="bold deep_sky_blue4")
    console.print("                  ██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗", justify="center", style="bold spring_green4")
    console.print("                  ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝██║  ███╗██║   ██║███████║██████╔╝██║  ██║", justify="center", style="bold spring_green4")
    console.print("                  ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║", justify="center", style="bold spring_green4")
    console.print("                  ███████║██║ ╚████║██║██║     ███████╗██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝", justify="center", style="bold deep_sky_blue4")
    console.print("                  ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝", justify="center", style="bold spring_green4")
    print("\n")
    console.rule("[bold underline red] Fet pel Grup 1 [/bold underline red]")




'''
def main():
Aquesta funció gestiona el flux principal del programa SniperGuard.
Mostra un menú a l'usuari per triar entre les opcions de Hardening, Cleaning o sortir del programa.
'''
def main():

    # Inicialitza el fitxer de log abans de qualsevol altra operació de registre
    init_log_file() 

    while True:
        log("==== SNIPERGUARD iniciant  ====", 200)
        log(f"PROJECT_ROOT = {PROJECT_ROOT}", 100)
        log(f"BASE_DIR = {BASE_DIR}", 100)
        log(f"LOGS_DIR = {LOGS_DIR}", 100)
        log(f"LOG_FILE({datetime.now().strftime('%Y-%m-%d')}) = {LOG_FILE}", 100)

        print_banner()
        print("\n")
        panel = Panel(
            Align.center("[bold green] Benvingut a SniperGuard, eina de Hardening i Cleaning  [/bold green]", vertical="middle"),
            style="on grey11",
            border_style="cyan",
            padding=(1, 6),
        )

        console.print(panel)
      
        if not check_admin_privileges():
            print()
            panel2 = Panel(
                Align.center("[bold red] ERROR! Aturant el programa. [/bold red]", vertical="middle"),
                style="on grey11",
                border_style="red",
                padding=(1, 6),
            )
            console.print(panel2)
            print("SniperGuard requereix ser executat com administrador per funcionar.")
            print("Si ets administrador, clica amb el botó dret sobre la icona de SniperGuard")
            print("i selecciona: 'Executa com a administrador'")
            print()
            log("SniperGuard s'ha aturat al no arrencar-se com administrador.",400)
            sys.exit()

        # Si el programa s'ha arrencat correctament, 
        # executem SniperGuard com a administrador.    
        log("SniperGuard s'ha executat correctament amb privilegis administratius.",250)
       
        while True:
            print("\n")
            table = Table(
                show_lines=True,           
                header_style="bold white",
                padding=(0, 1),
            )
            console.print("[bold underline green]Executant programa amb permisos d'administrador [bold underline green]")
            print()

            console.print("Escolleix una opció:", style="underline bold")
            table.add_column("ID", justify="center", header_style="bold white", no_wrap=True)
            table.add_column("Títol", justify="center", header_style="bold white")
            table.add_column("Descripció", justify="center",header_style="bold white")

            table.add_row("1.", "Hardening (Bastionatge)","Permet actualitzar el seu PC", style="bold yellow")
            table.add_row("2.", "Neteja i manteniment","Permet netejar arxius residuals del seu PC.",style="bold green")
            table.add_row("3.", "Gestió de logs","Permet comprimir, descomprimir i esborrar logs de SniperGuard",style="bold sky_blue1")
            table.add_row("4.", "Sons FX","Permet activar el sons FX de SniperGuard ",style="bold orange3")
            table.add_row("5.", "Sortir","Atura l'execució de SniperGuard", style="bold red")

            console.print(table)
            print("\n")

            try:
                decisio = check_input_user("Introdueix una opció : ", {"1", "2", "3", "4", "5"})
            except Exception as e:
                log(f"Error en check_input_user(): {e}", 400)
                decisio = None

            if decisio == "1":
                log("Hardening seleccionat", 250)
                try:
                    mode = choose_hardening_mode()
                    if mode is None:
                        break
                    hardening_menu(mode)
                    
                   
                except Exception as e:
                    log(f"Error executant Hardening: {e}", 400)
                    print("Error executant Hardening. Revisa els logs.")
                break

            elif decisio == "2":
                log("Cleaning seleccionat", 250)
                print("\n")
                try:
                    mode = choose_mode()
                    if mode is None:
                        break
                    cleaning_menu(mode)
                except Exception as e:
                    log(f"Error executant Cleaning: {e}", 400)
                    print("Error executant Cleaning. Revisa els logs.")
                break
            elif decisio == "3":
                log("Gestió de logs seleccionada", 250)
                print("\n")
                try:
                    mode = choose_logs()
                    if mode is None:
                        break
                except Exception as e:
                    log(f"Error executant Gestió de logs: {e}", 400)
                    print("Error executant Gestió de logs. Revisa els logs.")
                break
            elif decisio == "4":
                log("Secció sons FX", 250)
                print("\n")
                #
                try:
                    mode = sons_FX()
                    if mode is None:
                        break
                except Exception as e:
                    log(f"Error executant Gestió de logs: {e}", 400)
                    print("Error executant Gestió de logs. Revisa els logs.")
                break
            else:
                recursos.play_sound("shell.wav")
                log("Usuari ha sortit del programa (Exit).", 200)
                log("==== Fi SniperGuard ====", 200)
                show_log_link() # Mostra l'enllaç al fitxer de log abans de sortir
                return

# Punt d'entrada principal del programa
if __name__ == "__main__":
    try:
        main()
    
    except KeyboardInterrupt: # Ctrl+C
        log("Programa interromput per l'usuari (Ctrl+C)", 300)
        show_log_link() 
        print("\n[bold yellow]Programa aturat.[/bold yellow]")
    except Exception as e: # Altres excepcions no previstes
        log(f"Error en la execució main: {e}", 400)
        show_log_link()  
        console.print(f"[bold red]Error crític: {e}[/bold red]")