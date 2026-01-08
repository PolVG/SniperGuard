#Llibreries externes
import tkinter as tk
from PIL import Image, ImageTk
import time
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime

#Llibreries internes
import main
import recursos
from recursos import play_sound
from modules.LogRegister import init_log_file, CURRENT_LOG_FILE


#Plantilla de Colors utilitzats
COL_BG = "#0B0F14"
COL_SIDEBAR = "#121926"
COL_PANEL = "#161F2E"
COL_BORDER = "#2A3A52"
COL_TEXT = "#F2F5F9"
COL_MUTED = "#B7C0CC"
COL_ACCENT = "#4CC9F0"
COL_ACCENT_DARKTXT = "#061018"
COL_BTN = "#1B2638"
COL_BTN_HOVER = "#23314A"
COL_DANGER = "#FF5A5F"
COL_OK = "#2BD576"
PROGRESSBAR_THEME = "clam"

'''
Font Paraules
'''
FONT_UI = ("Segoe UI", 11)
FONT_UI_BOLD = ("Segoe UI", 11, "bold")
FONT_TITLE = ("Segoe UI", 11, "bold")

window = tk.Tk()

'''
Inicialitzar GUI
'''
window.title("SniperGuard")
window.geometry("900x700")
window.resizable(False, False)
window.configure(bg=COL_BG)


style = ttk.Style()
style.theme_use(PROGRESSBAR_THEME)
style.configure(
    "Sniper.Horizontal.TProgressbar",
    troughcolor=COL_PANEL,
    background=COL_ACCENT,
    bordercolor=COL_BORDER,
    lightcolor=COL_ACCENT,
    darkcolor=COL_ACCENT,
)

# Configuració de la quadrícula principal
window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=0)
window.rowconfigure(1, weight=1)


sidebar_frame = tk.Frame(window, bg=COL_SIDEBAR, width=150)
sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="ns")
sidebar_frame.grid_propagate(False)


# --- FALTA COMENTAR ---
cleaning_screen = tk.Frame(window, bg=COL_BG)
hardening_screen = tk.Frame(window, bg=COL_BG)
sound_screen = tk.Frame(window, bg=COL_BG)
#pantalla settings 
settings_screen = tk.Frame(window, bg=COL_BG)

cleaning_screen.grid(row=1, column=1, sticky="nsew")
hardening_screen.grid(row=1, column=1, sticky="nsew")
sound_screen.grid(row=1, column=1, sticky="nsew")
settings_screen.grid(row=1, column=1, sticky="nsew") 

IMG_WID = 70
IMG_HGT = 70


def add_hover(widget, normal_bg, hover_bg):
    def on_enter(event):
        widget.config(bg=hover_bg)

    def on_leave(event):
        widget.config(bg=normal_bg)

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def crear_avis(message):
    def cmd():
        messagebox.showinfo("Informació", message)
    return cmd


def create_sidebar_button(parent, image_path, command, padding=(10, 10), bg_color=None, hover_color=None):
    img = Image.open(image_path)
    img_resized = img.resize((IMG_WID, IMG_HGT))
    photo = ImageTk.PhotoImage(img_resized)

    btn = tk.Button(
        parent,
        image=photo,
        bg=bg_color,
        activebackground=hover_color,
        relief="flat",
        bd=0,
        highlightthickness=0,
        command=command,
    )
    btn.image = photo
    btn.pack(pady=padding[0], padx=padding[1])
    add_hover(btn, bg_color, hover_color)
    return btn


banner_label = tk.Label(
    window,
    text="NETEJA",
    bg=COL_BG,
    fg=COL_ACCENT,
    font=("Segoe UI", 28, "bold"),
)
banner_label.grid(row=0, column=1, sticky="n", pady=(14, 0))


def show_screen(name):
    if name == "hardening":
        hardening_screen.tkraise()
        banner_label.config(text="HARDENING")
    elif name == "sound":
        sound_screen.tkraise()
        banner_label.config(text="SONS FX")
    elif name == "settings":
        settings_screen.tkraise()
        banner_label.config(text="SETTINGS")
    else:
        cleaning_screen.tkraise()
        banner_label.config(text="NETEJA")


logo_img = Image.open("img/SniperGuardLogo.png")
logo_resized = logo_img.resize((IMG_WID, IMG_HGT))
logo_photo = ImageTk.PhotoImage(logo_resized)
logo_label = tk.Label(sidebar_frame, image=logo_photo, bg=COL_SIDEBAR)
logo_label.image = logo_photo
logo_label.pack(pady=10, padx=10)

sidebar_buttons = [
    ("img/cleaner_sin_fondo.png", lambda: show_screen("cleaning")),
    ("img/registry_sin_nombre.png", lambda: show_screen("hardening")),
    ("img/herramientas_sin_fondo.png", lambda: show_screen("sound")),
    ("img/opciones_sin_fondo.png", lambda: show_screen("settings")),
    ]

for img_path, cmd in sidebar_buttons:
    create_sidebar_button(
        sidebar_frame,
        img_path,
        cmd,
        padding=(10, 10),
        bg_color=COL_SIDEBAR,
        hover_color=COL_BTN_HOVER,
    )

show_screen("cleaning")


# ------------------------------------------------------------
# Cleaning screen UI
# ------------------------------------------------------------
main_container = tk.Frame(cleaning_screen, bg=COL_BG)
main_container.grid(row=0, column=0, sticky="nsew")
main_container.rowconfigure(0, weight=1)
main_container.columnconfigure(0, weight=1)

center_frame = tk.Frame(main_container, bg=COL_BG)
center_frame.grid(row=0, column=0)

progress_bar = ttk.Progressbar(
    center_frame,
    orient="horizontal",
    length=600,
    mode="determinate",
    style="Sniper.Horizontal.TProgressbar",
)
progress_bar.grid(row=0, column=0, pady=(20, 0))

progress_label = tk.Label(
    center_frame,
    text="0%",
    bg=COL_BG,
    fg=COL_TEXT,
    font=("Segoe UI", 14, "bold"),
)
progress_label.grid(row=1, column=0, pady=6)

content_frame = tk.Frame(center_frame, bg=COL_BG)
content_frame.grid(row=2, column=0, pady=10)

buttons_frame = tk.Frame(content_frame, bg=COL_BG)
buttons_frame.grid(row=0, column=0, sticky="n", padx=(0, 20))

panels_frame = tk.Frame(content_frame, bg=COL_BG)
panels_frame.grid(row=0, column=1, sticky="n")
panels_frame.columnconfigure(0, weight=1)

def reset_gui():
    progress_bar["value"] = 0
    progress_label.config(text="0%")
    logs_text.delete("1.0", tk.END)

    start_button.config(state="normal")

    deleted_label.grid_remove()
    kept_label.grid_remove()


def execute_action_temp(action_id: str, run_callback):
    deleted_label.grid_remove()
    kept_label.grid_remove()

    start_button.config(state="disabled")
    logs_text.delete("1.0", tk.END)

    log_path = init_log_file()
    log_file_path = log_path

    try:
        run_callback()

        with open(log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        total = len(lines)
        if total == 0:
            logs_text.insert(tk.END, "Arxiu buit.\n")
            return

        for i, line in enumerate(lines):
            current_percent = int(((i + 1) / total) * 100)
            progress_bar["value"] = current_percent
            progress_label.config(text=f"{current_percent}%")

            logs_text.insert(tk.END, line)
            logs_text.see(tk.END)

            window.update()
            time.sleep(0.01)

    except Exception as e:
        messagebox.showerror("Error", f"S'ha produït un error executant l'acció.\n{e}")
    finally:
        start_button.config(state="normal")


selected_position_var = tk.StringVar(value="2.1")
selected_mode_var = tk.StringVar(value="1")
selected_action_var = tk.StringVar(value="1")

def run_selected_cleaning():
    action = selected_action_var.get()
    mode_choice = selected_mode_var.get()

    if mode_choice not in {"1", "2"}:
        messagebox.showerror("Error", "Mode no vàlid.")
        return

    if action not in {"1", "2", "3"}:
        messagebox.showerror("Error", "Acció no vàlida.")
        return

    action_id = f"2.{mode_choice}.{action}"

    def callback():
        main.run_cleaning_from_gui(mode_choice, action)

    execute_action_temp(action_id, callback)


options_label = tk.Label(buttons_frame, text="Opcions", bg=COL_BG, fg=COL_TEXT, font=FONT_TITLE)
options_label.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="w")

start_button = tk.Button(
    buttons_frame,
    text="Iniciar",
    command=run_selected_cleaning,
    font=FONT_UI_BOLD,
    width=18,
    bg=COL_ACCENT,
    fg=COL_ACCENT_DARKTXT,
    activebackground="#7BE3FF",
    activeforeground=COL_ACCENT_DARKTXT,
    relief="flat",
    bd=0,
    highlightthickness=0,
)
start_button.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")
add_hover(start_button, COL_ACCENT, "#7BE3FF")

advanced_label = tk.Label(
    buttons_frame,
    text="Opcions avançades",
    bg=COL_BG,
    fg=COL_TEXT,
    font=FONT_TITLE,
)
advanced_label.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="w")

position_frame = tk.Frame(buttons_frame, bg=COL_BG)
position_frame.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")

tk.Label(position_frame, text="Posició:", bg=COL_BG, fg=COL_MUTED, font=FONT_UI).grid(row=0, column=0, sticky="w")

tk.Radiobutton(
    position_frame,
    text="2.1 Neteja",
    variable=selected_position_var,
    value="2.1",
    bg=COL_BG,
    fg=COL_TEXT,
    selectcolor=COL_PANEL,
    activebackground=COL_BG,
    activeforeground=COL_TEXT,
).grid(row=1, column=0, sticky="w")

mode_frame = tk.Frame(buttons_frame, bg=COL_BG)
mode_frame.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="w")

tk.Label(mode_frame, text="Mode:", bg=COL_BG, fg=COL_MUTED, font=FONT_UI).grid(row=0, column=0, sticky="w")

tk.Radiobutton(
    mode_frame,
    text="Identificar (BAR)",
    variable=selected_mode_var,
    value="1",
    bg=COL_BG,
    fg=COL_TEXT,
    selectcolor=COL_PANEL,
    activebackground=COL_BG,
    activeforeground=COL_TEXT,
).grid(row=1, column=0, sticky="w")

tk.Radiobutton(
    mode_frame,
    text="Identificar i eliminar (DEL)",
    variable=selected_mode_var,
    value="2",
    bg=COL_BG,
    fg=COL_TEXT,
    selectcolor=COL_PANEL,
    activebackground=COL_BG,
    activeforeground=COL_TEXT,
).grid(row=2, column=0, sticky="w")

action_frame = tk.Frame(buttons_frame, bg=COL_BG)
action_frame.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="w")

tk.Label(action_frame, text="Acció:", bg=COL_BG, fg=COL_MUTED, font=FONT_UI).grid(row=0, column=0, sticky="w")

tk.Radiobutton(
    action_frame,
    text="Temporals",
    variable=selected_action_var,
    value="1",
    bg=COL_BG,
    fg=COL_TEXT,
    selectcolor=COL_PANEL,
    activebackground=COL_BG,
    activeforeground=COL_TEXT,
).grid(row=1, column=0, sticky="w")

tk.Radiobutton(
    action_frame,
    text="Navegadors",
    variable=selected_action_var,
    value="2",
    bg=COL_BG,
    fg=COL_TEXT,
    selectcolor=COL_PANEL,
    activebackground=COL_BG,
    activeforeground=COL_TEXT,
).grid(row=2, column=0, sticky="w")

tk.Radiobutton(
    action_frame,
    text="Paperera",
    variable=selected_action_var,
    value="3",
    bg=COL_BG,
    fg=COL_TEXT,
    selectcolor=COL_PANEL,
    activebackground=COL_BG,
    activeforeground=COL_TEXT,
).grid(row=3, column=0, sticky="w")

status_frame = tk.Frame(buttons_frame, bg=COL_BG)
status_frame.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="w")

deleted_label = tk.Label(status_frame, text="Fitxers eliminats", font=FONT_UI, bg=COL_BG, fg=COL_DANGER)
kept_label = tk.Label(status_frame, text="Fitxers conservats", font=FONT_UI, bg=COL_BG, fg=COL_OK)

deleted_label.grid(row=0, column=0, sticky="w")
kept_label.grid(row=1, column=0, sticky="w")
deleted_label.grid_remove()
kept_label.grid_remove()

logs_label = tk.Label(panels_frame, text="Tots els logs", bg=COL_BG, fg=COL_TEXT, font=FONT_TITLE)
logs_label.grid(row=0, column=0, padx=10, pady=(0, 0), sticky="w")

logs_text = tk.Text(
    panels_frame,
    bg=COL_PANEL,
    fg=COL_TEXT,
    insertbackground=COL_TEXT,
    height=23,
    width=60,
    font=("Consolas", 10),
    relief="flat",
    highlightthickness=1,
    highlightbackground=COL_BORDER,
)
logs_text.grid(row=1, column=0, padx=10, pady=(10, 0))


# --- FALTA COMENTAR ---
hard_main = tk.Frame(hardening_screen, bg=COL_BG)
hard_main.pack(fill="both", expand=True)

hard_left = tk.Frame(hard_main, bg=COL_BG)
hard_left.pack(side="left", anchor="n", padx=(40, 10), pady=(40, 10))

hard_right = tk.Frame(hard_main, bg=COL_BG)
hard_right.pack(side="left", anchor="n", padx=(10, 10), pady=(40, 10))

hard_title = tk.Label(
    hard_left,
    text="Opcions Hardening",
    bg=COL_BG,
    fg=COL_TEXT,
    font=("Segoe UI", 16, "bold"),
)
hard_title.grid(row=0, column=0, sticky="w", pady=(0, 15))

hard_mode_var = tk.StringVar(value="BAR")
hard_action_var = tk.StringVar(value="1")

# --- FALTA COMENTAR ---
hard_logs_label = tk.Label(
    hard_right,
    text="Tots els logs (Hardening)",
    bg=COL_BG,
    fg=COL_TEXT,
    font=FONT_TITLE,
)
hard_logs_label.pack(anchor="w")

hard_logs_text = tk.Text(
    hard_right,
    bg=COL_PANEL,
    fg=COL_TEXT,
    insertbackground=COL_TEXT,
    height=23,
    width=60,
    font=("Consolas", 10),
    relief="flat",
    highlightthickness=1,
    highlightbackground=COL_BORDER,
)
hard_logs_text.pack(pady=(10, 0))


# --- FALTA COMENTAR ---
def execute_action_hard(action_id: str, run_callback):
    hard_start_button.config(state="disabled")
    hard_logs_text.delete("1.0", tk.END)

    log_path = init_log_file()
    log_file_path = log_path

    try:
        run_callback()

        with open(log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        total = len(lines)
        if total == 0:
            hard_logs_text.insert(tk.END, "Arxiu buit.\n")
            return

        for i, line in enumerate(lines):
            current_percent = int(((i + 1) / total) * 100)
            progress_bar["value"] = current_percent
            progress_label.config(text=f"{current_percent}%")

            hard_logs_text.insert(tk.END, line)
            hard_logs_text.see(tk.END)

            window.update()
            time.sleep(0.01)

    except Exception as e:
        messagebox.showerror("Error", f"S'ha produït un error executant l'acció.\n{e}")
    finally:
        hard_start_button.config(state="normal")


def refresh_hardening_actions():
    for w in hard_action_frame.winfo_children():
        w.destroy()

    tk.Label(hard_action_frame, text="Acció:", bg=COL_BG, fg=COL_MUTED, font=FONT_UI).grid(row=0, column=0, sticky="w")

    if hard_mode_var.get() == "BAR":
        tk.Radiobutton(hard_action_frame, text="Defender està actiu", variable=hard_action_var, value="1",
                       bg=COL_BG, fg=COL_TEXT, selectcolor=COL_PANEL, activebackground=COL_BG, activeforeground=COL_TEXT).grid(row=1, column=0, sticky="w")
        tk.Radiobutton(hard_action_frame, text="Defender: updates disponibles", variable=hard_action_var, value="2",
                       bg=COL_BG, fg=COL_TEXT, selectcolor=COL_PANEL, activebackground=COL_BG, activeforeground=COL_TEXT).grid(row=2, column=0, sticky="w")
        tk.Radiobutton(hard_action_frame, text="Windows Update: comprovar", variable=hard_action_var, value="3",
                       bg=COL_BG, fg=COL_TEXT, selectcolor=COL_PANEL, activebackground=COL_BG, activeforeground=COL_TEXT).grid(row=3, column=0, sticky="w")
    else:
        tk.Radiobutton(hard_action_frame, text="Actualitzar Windows Defender", variable=hard_action_var, value="1",
                       bg=COL_BG, fg=COL_TEXT, selectcolor=COL_PANEL, activebackground=COL_BG, activeforeground=COL_TEXT).grid(row=1, column=0, sticky="w")
        tk.Radiobutton(hard_action_frame, text="Executar Windows Update", variable=hard_action_var, value="2",
                       bg=COL_BG, fg=COL_TEXT, selectcolor=COL_PANEL, activebackground=COL_BG, activeforeground=COL_TEXT).grid(row=2, column=0, sticky="w")


def run_selected_hardening():
    mode = hard_mode_var.get()
    action = hard_action_var.get()

    if mode == "BAR":
        scripts = {
            "1": "HARD_WinDefender.py",
            "2": "HARD_WinDefenderUpdateAvailable.py",
            "3": "BAR_test5_UPDATE.py",
        }
    else:
        scripts = {
            "1": "HARD_WinDefenderUpdate.py",
            "2": "HARD_WindowsUpdate.py",
        }

    if action not in scripts:
        messagebox.showerror("Error", "Acció hardening no vàlida.")
        return

    script = scripts[action]

    def callback():
        main.run_script(script)

    execute_action_hard(f"HARD.{mode}.{action}", callback)


hard_start_button = tk.Button(
    hard_left,
    text="Iniciar",
    command=run_selected_hardening,
    font=FONT_UI_BOLD,
    width=18,
    bg=COL_ACCENT,
    fg=COL_ACCENT_DARKTXT,
    activebackground="#7BE3FF",
    activeforeground=COL_ACCENT_DARKTXT,
    relief="flat",
    bd=0,
    highlightthickness=0,
)
hard_start_button.grid(row=1, column=0, sticky="w", pady=(0, 20))
add_hover(hard_start_button, COL_ACCENT, "#7BE3FF")

hard_mode_frame = tk.Frame(hard_left, bg=COL_BG)
hard_mode_frame.grid(row=2, column=0, sticky="w")

tk.Label(hard_mode_frame, text="Mode:", bg=COL_BG, fg=COL_MUTED, font=FONT_UI).grid(row=0, column=0, sticky="w")

tk.Radiobutton(
    hard_mode_frame,
    text="Identificar (BAR)",
    variable=hard_mode_var,
    value="BAR",
    command=refresh_hardening_actions,
    bg=COL_BG,
    fg=COL_TEXT,
    selectcolor=COL_PANEL,
    activebackground=COL_BG,
    activeforeground=COL_TEXT,
).grid(row=1, column=0, sticky="w")

tk.Radiobutton(
    hard_mode_frame,
    text="Aplicar (HARD)",
    variable=hard_mode_var,
    value="HARD",
    command=refresh_hardening_actions,
    bg=COL_BG,
    fg=COL_TEXT,
    selectcolor=COL_PANEL,
    activebackground=COL_BG,
    activeforeground=COL_TEXT,
).grid(row=2, column=0, sticky="w")

hard_action_frame = tk.Frame(hard_left, bg=COL_BG)
hard_action_frame.grid(row=3, column=0, sticky="w", pady=(12, 0))

refresh_hardening_actions()


# --- FALTA COMENTAR ---
sound_frame = tk.Frame(sound_screen, bg=COL_BG)
sound_frame.pack(fill="both", expand=True)

sound_title = tk.Label(
    sound_frame,
    text="Sons FX",
    bg=COL_BG,
    fg=COL_ACCENT,
    font=("Segoe UI", 22, "bold"),
)
sound_title.pack(pady=(40, 10))

sound_desc = tk.Label(
    sound_frame,
    text="Activa o desactiva els sons del programa.",
    bg=COL_BG,
    fg=COL_MUTED,
    font=FONT_UI,
)
sound_desc.pack(pady=(0, 20))

# --- FALTA COMENTAR ---
if not hasattr(recursos, "SOUND_ENABLED"):
    recursos.SOUND_ENABLED = False

sound_enabled_var = tk.BooleanVar(value=bool(recursos.SOUND_ENABLED))

# --- FALTA COMENTAR ---
def toggle_sound():
    recursos.SOUND_ENABLED = bool(sound_enabled_var.get())
    if recursos.SOUND_ENABLED:
        try:
            play_sound("reloading.wav")
        except Exception:
            pass

sound_check = tk.Checkbutton(
    sound_frame,
    text="Activar Sons FX",
    variable=sound_enabled_var,
    command=toggle_sound,
    bg=COL_BG,
    fg=COL_TEXT,
    selectcolor=COL_PANEL,
    activebackground=COL_BG,
    activeforeground=COL_TEXT,
    font=FONT_UI_BOLD,
)
sound_check.pack()















#Funciones para el texto de la resolucion y la posicion actual de la barra deslizadora
#estas funciones las voy a llamar luego cuando programe los botones 
def cambiar_resolucion(resolucion_seleccionada):
    window.geometry(resolucion_seleccionada)

def ajustar_volumen(valor):
    volumen = int(valor)
    if volumen == 0:
        recursos.SOUND_ENABLED = False
    else:
        recursos.SOUND_ENABLED = True
    
#esto servira para abrir la carpeta donde se guardan los logs
def obrir_logs():
    import os
    log_dir = Path("logs") # esto es para comprobar si la carpeta existe
    if not log_dir.exists():
        log_dir.mkdir()
    os.startfile(log_dir.resolve())


#Contenido de la pantalla Ajustes
settings_container = tk.Frame(settings_screen, bg=COL_BG)
settings_container.pack(fill="both", expand=True, padx=50, pady=50)

#seleccionar size de la interfaz 
tk.Label(
    settings_container, text="Resolucio de la pantalla", 
    bg=COL_BG, fg=COL_TEXT, font=FONT_TITLE
).pack(anchor="w", pady=(0, 10))

# Menú desplegable para el tamaño
opciones_resolucion = ["900x700", "1024x768", "1280x720", "800x600"] #las opciones de resolucion
var_resolucion = tk.StringVar(value="900x700")  #se pueden añadir maas

menu_res = tk.OptionMenu(
    settings_container, var_resolucion, *opciones_resolucion, 
    command=cambiar_resolucion #llamo a la funcion anterior para poner la resolución a la que se ha cambiado
)
menu_res.config(
    bg=COL_BTN, fg=COL_TEXT, highlightthickness=0, 
    activebackground=COL_BTN_HOVER, relief="flat", 
    font=FONT_UI, width=15
)
menu_res["menu"].config(bg=COL_PANEL, fg=COL_TEXT, font=FONT_UI)
menu_res.pack(anchor="w", pady=(0, 40))

# seleccionar volumen 
tk.Label(
    settings_container, text="Volum del programa", 
    bg=COL_BG, fg=COL_TEXT, font=FONT_TITLE
).pack(anchor="w", pady=(0, 10))

# Barra deslizadora para el volumen
slider_volumen = tk.Scale(
    settings_container,
    from_=0, to=100,
    orient="horizontal",
    bg=COL_BG,
    fg=COL_MUTED,
    troughcolor=COL_PANEL,
    activebackground=COL_ACCENT,
    highlightthickness=0,
    length=400,
    font=FONT_UI,
    command=ajustar_volumen #llamo a la funcion aqui
)
slider_volumen.set(50) # Valor inicial
slider_volumen.pack(anchor="w")

#texto que aparece debajo de la barra
tk.Label(
    settings_container, 
    text="Ajusta per activar o desactivar els efectes de so", 
    bg=COL_BG, fg=COL_MUTED, font=("Segoe UI", 9)
).pack(anchor="w", pady=(5, 0))


#Botones de Carpeta Logs y el tema 
tk.Label(settings_container, text="LOGS i Tema", bg=COL_BG, fg=COL_TEXT, font=FONT_TITLE).pack(anchor="w", pady=(10, 10))
#esto son los botones horizontales
btns_frame = tk.Frame(settings_container, bg=COL_BG)
btns_frame.pack(anchor="w")

#el boton para abrir los logs
btn_logs = tk.Button(btns_frame, text="Obrir carpeta de Logs 📁", command=obrir_logs, font=FONT_UI_BOLD, bg=COL_BTN, fg=COL_TEXT, relief="flat", padx=15, pady=5)
btn_logs.pack(side="left", padx=(0, 10))
add_hover(btn_logs, COL_BTN, COL_BTN_HOVER)


window.mainloop()