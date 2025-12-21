#Llibreries externes
import tkinter as tk
from PIL import Image, ImageTk
import time
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime

#Llibreries internes
import main
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

# ProgessBar configuració d'estil
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
window.columnconfigure(0, weight=0)   # sidebar
window.columnconfigure(1, weight=1)   # content
window.rowconfigure(0, weight=0)      # banner
window.rowconfigure(1, weight=1)      # content

# Barra Lateral
sidebar_frame = tk.Frame(window, bg=COL_SIDEBAR, width=150)
sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="ns")
sidebar_frame.grid_propagate(False)

# Redimensionament d'imatges per als botons
IMG_WID = 70
IMG_HGT = 70


# Funcions auxiliars
def add_hover(widget, normal_bg, hover_bg):
    def on_enter(event):
        widget.config(bg=hover_bg)

    def on_leave(event):
        widget.config(bg=normal_bg)

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def crear_avis(message):
    def cmd():
        messagebox.showinfo("Información", message)
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



logo_img = Image.open("img/SniperGuardLogo.png")
logo_resized = logo_img.resize((IMG_WID, IMG_HGT))
logo_photo = ImageTk.PhotoImage(logo_resized)
logo_label = tk.Label(sidebar_frame, image=logo_photo, bg=COL_SIDEBAR)
logo_label.image = logo_photo
logo_label.pack(pady=10, padx=10)

sidebar_buttons = [
    ("img/cleaner_sin_fondo.png", "Estas actualment aquesta pantalla."),
    ("img/registry_sin_nombre.png", "Boto en desenvolupament."),
    ("img/herramientas_sin_fondo.png", "Boto en desenvolupament."),
    ("img/opciones_sin_fondo.png", "Boto en desenvolupament."),
]

for img_path, msg in sidebar_buttons:
    cmd = crear_avis(msg)
    create_sidebar_button(
        sidebar_frame,
        img_path,
        cmd,
        padding=(10, 10),
        bg_color=COL_SIDEBAR,
        hover_color=COL_BTN_HOVER,
    )


banner_label = tk.Label(
    window,
    text="CLEANING",
    bg=COL_BG,
    fg=COL_ACCENT,
    font=("Segoe UI", 28, "bold"),
)
banner_label.grid(row=0, column=1, sticky="n", pady=(14, 0))


main_container = tk.Frame(window, bg=COL_BG)
main_container.grid(row=1, column=1, sticky="nsew")
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

    summary_text.delete("1.0", tk.END)
    logs_text.delete("1.0", tk.END)

    delete_button.config(state="disabled")
    keep_button.config(state="disabled")
    start_button.config(state="normal")

    deleted_label.grid_remove()
    kept_label.grid_remove()


def execute_action_temp(action_id: str, run_callback):
    deleted_label.grid_remove()
    kept_label.grid_remove()

    start_button.config(state="disabled")
    delete_button.config(state="disabled")
    keep_button.config(state="disabled")

    summary_text.delete("1.0", tk.END)
    logs_text.delete("1.0", tk.END)

    log_path = init_log_file()
    log_file_path = log_path

    try:
        run_callback()

        with open(log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            total = len(lines)

        if total == 0:
            summary_text.insert(tk.END, "Archivo vacío.")
            return

        sections = []
        current_section = None

        for i, line in enumerate(lines):
            current_percent = int(((i + 1) / total) * 100)
            progress_bar["value"] = current_percent
            progress_label.config(text=f"{current_percent}%")

            logs_text.insert(tk.END, line)
            logs_text.see(tk.END)

            text = line.strip()

            if text.startswith("="):
                name = text.strip("=").strip()
                if name:
                    current_section = {"nom": name}
                    sections.append(current_section)

            elif line.startswith("Ruta:") and current_section is not None:
                current_section["ruta"] = line.split("Ruta:", 1)[1].strip()

            elif line.lstrip().startswith("Mida total") and current_section is not None:
                current_section["mida_total"] = line.split(":", 1)[1].strip()

            elif line.lstrip().startswith("Fitxers") and current_section is not None:
                current_section["fitxers"] = line.split(":", 1)[1].strip()

            elif line.lstrip().startswith("Baròmetre") and current_section is not None:
                current_section["barometre"] = line.split(":", 1)[1].strip()

            window.update()
            time.sleep(0.03)

        summary_text.insert(tk.END, "RESUM DE L'ANÀLISI\n")
        summary_text.insert(tk.END, f"Acció: {action_id}\n")
        summary_text.insert(tk.END, f"Fitxer log: {log_path.name}\n")
        summary_text.insert(tk.END, "----------------------------------------\n")

        useful_sections = [s for s in sections if "ruta" in s]

        if not useful_sections:
            summary_text.insert(tk.END, "No s'ha trobat cap carpeta analitzada.\n")
        else:
            for sec in useful_sections:
                nom = sec.get("nom", "Secció")
                ruta = sec.get("ruta", "Desconeguda")
                mida = sec.get("mida_total", "Desconeguda")
                fitxers = sec.get("fitxers", "Desconegut")
                barometre = sec.get("barometre", "Sense dades")

                summary_text.insert(tk.END, f"{nom}\n")
                summary_text.insert(tk.END, f"  Ruta       : {ruta}\n")
                summary_text.insert(tk.END, f"  Mida total : {mida}\n")
                summary_text.insert(tk.END, f"  Fitxers    : {fitxers}\n")
                summary_text.insert(tk.END, f"  Baròmetre  : {barometre}\n")
                summary_text.insert(tk.END, "----------------------------------------\n")

        summary_text.see(tk.END)

    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo en: {log_file_path}")
    finally:
        start_button.config(state="normal")
        delete_button.config(state="normal")
        keep_button.config(state="normal")



selected_position_var = tk.StringVar(value="2.1") 
selected_mode_var = tk.StringVar(value="1")        
selected_action_var = tk.StringVar(value="1")     


def run_selected_cleaning():
    action = selected_action_var.get()      
    mode_choice = selected_mode_var.get()    

    
    action_id = f"2.{mode_choice}.{action}"

    def callback():
        main.run_cleaning_from_gui(mode_choice, action)

    execute_action_temp(action_id, callback)


def confirm_delete():
    question = messagebox.askquestion(
        "Eliminacion",
        "Los siguientes archivos seran eliminados.\n¿Está seguro?",
    )
    if question == "yes":
        try:
            keep_button.config(state="disabled")
            execute_action_temp("ID2.1.2", lambda: main.run_script("DEL_test1_TEMP.py"))
            deleted_label.grid_remove()
            kept_label.grid_remove()
            deleted_label.grid(row=0, column=0, sticky="w")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron eliminar los archivos. {e}")


def mark_keep():
    deleted_label.grid_remove()
    kept_label.grid_remove()
    kept_label.grid(row=1, column=0, sticky="w")


# Títol columna esquerra
options_label = tk.Label(buttons_frame, text="Opciones", bg=COL_BG, fg=COL_TEXT, font=FONT_TITLE)
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

keep_button = tk.Button(
    buttons_frame,
    text="Conservar",
    command=mark_keep,
    width=18,
    state="disabled",
    font=FONT_UI_BOLD,
    bg=COL_BTN,
    fg=COL_TEXT,
    activebackground=COL_BTN_HOVER,
    activeforeground=COL_TEXT,
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=COL_BORDER,
)
keep_button.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")

delete_button = tk.Button(
    buttons_frame,
    text="Eliminar",
    command=confirm_delete,
    width=18,
    state="disabled",
    font=FONT_UI_BOLD,
    bg=COL_BTN,
    fg=COL_TEXT,
    activebackground=COL_BTN_HOVER,
    activeforeground=COL_TEXT,
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=COL_BORDER,
)
delete_button.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")


advanced_label = tk.Label(
    buttons_frame,
    text="Opciones avanzadas",
    bg=COL_BG,
    fg=COL_TEXT,
    font=FONT_TITLE,
)
advanced_label.grid(row=4, column=0, padx=10, pady=(10, 5), sticky="w")


position_frame = tk.Frame(buttons_frame, bg=COL_BG)
position_frame.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="w")

tk.Label(position_frame, text="Posicion:", bg=COL_BG, fg=COL_MUTED, font=FONT_UI).grid(row=0, column=0, sticky="w")

tk.Radiobutton(
    position_frame,
    text="2.1 Cleaning",
    variable=selected_position_var,
    value="2.1",
    bg=COL_BG,
    fg=COL_TEXT,
    selectcolor=COL_PANEL,
    activebackground=COL_BG,
    activeforeground=COL_TEXT,
).grid(row=1, column=0, sticky="w")


mode_frame = tk.Frame(buttons_frame, bg=COL_BG)
mode_frame.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="w")

tk.Label(mode_frame, text="Modo:", bg=COL_BG, fg=COL_MUTED, font=FONT_UI).grid(row=0, column=0, sticky="w")

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
    text="Identificar y esborrar (DEL)",
    variable=selected_mode_var,
    value="2",
    bg=COL_BG,
    fg=COL_TEXT,
    selectcolor=COL_PANEL,
    activebackground=COL_BG,
    activeforeground=COL_TEXT,
).grid(row=2, column=0, sticky="w")

action_frame = tk.Frame(buttons_frame, bg=COL_BG)
action_frame.grid(row=7, column=0, padx=10, pady=(0, 10), sticky="w")

tk.Label(action_frame, text="Accion:", bg=COL_BG, fg=COL_MUTED, font=FONT_UI).grid(row=0, column=0, sticky="w")

tk.Radiobutton(
    action_frame,
    text="Temporales",
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
    text="Navegadores",
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
    text="Papelera",
    variable=selected_action_var,
    value="3",  
    bg=COL_BG,
    fg=COL_TEXT,
    selectcolor=COL_PANEL,
    activebackground=COL_BG,
    activeforeground=COL_TEXT,
).grid(row=3, column=0, sticky="w")


status_frame = tk.Frame(buttons_frame, bg=COL_BG)
status_frame.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="w")

deleted_label = tk.Label(status_frame, text="Archivos eliminados", font=FONT_UI, bg=COL_BG, fg=COL_DANGER)
kept_label = tk.Label(status_frame, text="Archivos conservados", font=FONT_UI, bg=COL_BG, fg=COL_OK)

deleted_label.grid(row=0, column=0, sticky="w")
kept_label.grid(row=1, column=0, sticky="w")
deleted_label.grid_remove()
kept_label.grid_remove()



summary_label = tk.Label(panels_frame, text="Resumen", bg=COL_BG, fg=COL_TEXT, font=FONT_TITLE)
summary_label.grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")

summary_text = tk.Text(
    panels_frame,
    bg=COL_PANEL,
    fg=COL_TEXT,
    insertbackground=COL_TEXT,
    height=10,
    width=60,
    font=("Consolas", 10),
    relief="flat",
    highlightthickness=1,
    highlightbackground=COL_BORDER,
)
summary_text.grid(row=1, column=0, padx=10, pady=(0, 10))

logs_label = tk.Label(panels_frame, text="Todos los logs", bg=COL_BG, fg=COL_TEXT, font=FONT_TITLE)
logs_label.grid(row=2, column=0, padx=10, pady=(15, 0), sticky="w")

logs_text = tk.Text(
    panels_frame,
    bg=COL_PANEL,
    fg=COL_TEXT,
    insertbackground=COL_TEXT,
    height=10,
    width=60,
    font=("Consolas", 10),
    relief="flat",
    highlightthickness=1,
    highlightbackground=COL_BORDER,
)
logs_text.grid(row=3, column=0, padx=10, pady=(10, 0))

add_hover(start_button, COL_ACCENT, "#7BE3FF")
add_hover(keep_button, COL_BTN, COL_BTN_HOVER)
add_hover(delete_button, COL_BTN, COL_BTN_HOVER)

window.mainloop()