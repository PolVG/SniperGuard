import tkinter as tk
from PIL import Image, ImageTk
import time
from tkinter import ttk, messagebox
import main
from pathlib import Path
from datetime import datetime
from modules.LogRegister import init_log_file, CURRENT_LOG_FILE

window = tk.Tk()
window.title("SniperGuard")
window.geometry("800x600")
window.resizable(False, False)
window.configure(bg="gray20")

window.columnconfigure(1, weight=1)
window.rowconfigure(1, weight=1)

# barra Lateral
barra_lateral = tk.Frame(window, bg="#9D9CA8", width=150)
barra_lateral.grid(row=0, column=0, rowspan=2, sticky='ns')
barra_lateral.grid_propagate(False)

#boton 1
boton1 = Image.open("img/SniperGuardLogo.png")
NUEVO_ANCHO = 70
NUEVO_ALTO = 70
boton1_redimensionado = boton1.resize((NUEVO_ANCHO, NUEVO_ALTO), Image.LANCZOS)
imagen_del_boton = ImageTk.PhotoImage(boton1_redimensionado)
boton1_imagen_unico = tk.Button(
    barra_lateral,
    image=imagen_del_boton,
    bg="#9D9CA8",
    relief="flat",
    command=lambda: print("Home")
)
boton1_imagen_unico.image = imagen_del_boton
boton1_imagen_unico.pack(pady=10, padx=10, fill='x')

#boton2
boton2 = Image.open("img/cleaner_sin_fondo.png")
boton2_redimensionado = boton2.resize((NUEVO_ANCHO, NUEVO_ALTO), Image.LANCZOS)
imagen_del_boton = ImageTk.PhotoImage(boton2_redimensionado)
boton2_imagen_unico = tk.Button(
    barra_lateral,
    image=imagen_del_boton,
    bg="#9D9CA8",
    relief="flat",
    command=lambda: print("CLEANER clicked")
)
boton2_imagen_unico.image = imagen_del_boton
boton2_imagen_unico.pack(pady=10, padx=10, fill='x')

#boton3
boton3 = Image.open("img/registry_sin_nombre.png")
boton3_redimensionado = boton3.resize((NUEVO_ANCHO, NUEVO_ALTO), Image.LANCZOS)
imagen_del_boton = ImageTk.PhotoImage(boton3_redimensionado)
boton3_imagen_unico = tk.Button(
    barra_lateral,
    image=imagen_del_boton,
    bg="#9D9CA8",
    relief="flat",
    command=lambda: print("REGISTRY clicked")
)
boton3_imagen_unico.image = imagen_del_boton
boton3_imagen_unico.pack(pady=10, padx=10, fill='x')

#boton4
boton4 = Image.open("img/herramientas_sin_fondo.png")
boton4_redimensionado = boton3.resize((NUEVO_ANCHO, NUEVO_ALTO), Image.LANCZOS)
imagen_del_boton = ImageTk.PhotoImage(boton3_redimensionado)
boton4_imagen_unico = tk.Button(
    barra_lateral,
    image=imagen_del_boton,
    bg="#9D9CA8",
    relief="flat",
    command=lambda: print("HERRAMIENTAS clicked")
)
boton4_imagen_unico.image = imagen_del_boton
boton4_imagen_unico.pack(pady=10, padx=10, fill='x')

#boton5
boton5 = Image.open("img/opciones_sin_fondo.png")
boton5_redimensionado = boton5.resize((NUEVO_ANCHO, NUEVO_ALTO), Image.LANCZOS)
imagen_del_boton = ImageTk.PhotoImage(boton5_redimensionado)
boton5_imagen_unico = tk.Button(
    barra_lateral,
    image=imagen_del_boton,
    bg="#9D9CA8",
    relief="flat",
    command=lambda: print("OPCIONES clicked")
)
boton5_imagen_unico.image = imagen_del_boton
boton5_imagen_unico.pack(pady=10, padx=10, fill='x')

# banner de sniperguard
banner = Image.open("img/banersinlogo.png")
banner_redimensionado = banner.resize((650, 100), Image.LANCZOS)
imagen_banner = ImageTk.PhotoImage(banner_redimensionado)
label_del_banner = tk.Label(window, image=imagen_banner, bg="gray20")
label_del_banner.grid(row=0, column=1, sticky='nwe')
label_del_banner.image = imagen_banner

contenedor_principal = tk.Frame(window, bg="gray20")
contenedor_principal.grid(row=1, column=1, sticky="nsew", padx=20)

progreso = ttk.Progressbar(contenedor_principal, orient="horizontal", length=500, mode="determinate")
progreso.grid(row=0, column=0, pady=(20, 0))

label_porcentaje = tk.Label(
    contenedor_principal,
    text="0%",
    bg="gray20",
    fg="#9D9CA8",
    font=("Impact", 15, "bold")
)
label_porcentaje.grid(row=1, column=0, pady=5)

# ─ Frame principal: botons (esquerra) + requadres (dreta) ─ #
frame_main = tk.Frame(contenedor_principal, bg="gray20")
frame_main.grid(row=2, column=0, pady=10, sticky="nsew")

# Columnes del frame principal
frame_main.columnconfigure(0, weight=0)  # botons
frame_main.columnconfigure(1, weight=1)  # requadres

# Esquerra: frame per als botons
frame_botons = tk.Frame(frame_main, bg="gray20")
frame_botons.grid(row=0, column=0, sticky="n")

# Dreta: frame per als requadres (resum + logs)
frame_requadres = tk.Frame(frame_main, bg="gray20")
frame_requadres.grid(row=0, column=1, sticky="nsew")

# files: 0 = títol Resumen, 1 = quadre Resum,
#        2 = títol Todos los logs, 3 = quadre Logs
frame_requadres.rowconfigure(0, weight=0)
frame_requadres.rowconfigure(1, weight=1)
frame_requadres.rowconfigure(2, weight=0)
frame_requadres.rowconfigure(3, weight=1)
frame_requadres.columnconfigure(0, weight=1)

def reset_gui():
    """Retorna la GUI a l'estat inicial (sense resultats)."""
    progreso['value'] = 0
    label_porcentaje.config(text="0%")

    arch_encontrados.delete('1.0', tk.END)
    logs.delete('1.0', tk.END)

    btn_el.config(state="disabled")
    btn_cons.config(state="disabled")
    boton_iniciar.config(state="normal")

    arch_eliminados.grid_forget()
    arch_conservados.grid_forget()

def executar_accio_temp(action_id: str, run_callback):
    """
    Funció comuna per executar una acció sobre temporals (BAR o DEL),
    escriure el log i mostrar-lo a la GUI.
    """
    # Amaguem missatges previs
    arch_conservados.grid_forget()
    arch_eliminados.grid_forget()

    # Desactivar botons mentre treballem
    boton_iniciar.config(state="disabled")
    btn_el.config(state="disabled")
    btn_cons.config(state="disabled")

    # Netejar quadres
    arch_encontrados.delete('1.0', tk.END)
    logs.delete('1.0', tk.END)

    # Crear fitxer de log per aquesta execució
    log_path = init_log_file()
    LOG_FILE = log_path

    try:
        # Executar la lògica (BAR o DEL)
        run_callback()

        # Llegir el log generat
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lineas = f.readlines()
            total = len(lineas)

        if total == 0:
            arch_encontrados.insert(tk.END, "Archivo vacío.")
            return

        seccions = []
        seccio_actual = None
        
 

        for i, linea in enumerate(lineas):
            porcentaje_actual = int(((i + 1) / total) * 100)
            progreso['value'] = porcentaje_actual
            label_porcentaje.config(text=f"{porcentaje_actual}%")

            # Logs complets
            logs.insert(tk.END, linea)
            logs.see(tk.END)

            text = linea.strip()

            # Seccions de resum (línies amb ==== ...)
            if text.startswith("="):
                nom = text.strip("=").strip()
                if nom:
                    seccio_actual = {"nom": nom}
                    seccions.append(seccio_actual)

            # Extreure camps rellevants de cada secció
            elif linea.startswith("Ruta:") and seccio_actual is not None:
                seccio_actual["ruta"] = linea.split("Ruta:", 1)[1].strip()

            elif linea.lstrip().startswith("Mida total") and seccio_actual is not None:
                seccio_actual["mida_total"] = linea.split(":", 1)[1].strip()

            elif linea.lstrip().startswith("Fitxers") and seccio_actual is not None:
                seccio_actual["fitxers"] = linea.split(":", 1)[1].strip()

            elif linea.lstrip().startswith("Baròmetre") and seccio_actual is not None:
                seccio_actual["barometre"] = linea.split(":", 1)[1].strip()

            window.update()
            time.sleep(0.05)

        # Resum al quadre superior
        arch_encontrados.insert(tk.END, "RESUM DE L'ANÀLISI\n")
        arch_encontrados.insert(tk.END, f"Acció: {action_id}\n")
        arch_encontrados.insert(tk.END, f"Fitxer log: {log_path.name}\n")
        arch_encontrados.insert(tk.END, "----------------------------------------\n")

        seccions_utiles = [s for s in seccions if "ruta" in s]

        if not seccions_utiles:
            arch_encontrados.insert(tk.END, "No s'ha trobat cap carpeta analitzada.\n")
        else:
            for sec in seccions_utiles:
                nom = sec.get("nom", "Secció")
                ruta = sec.get("ruta", "Desconeguda")
                mida = sec.get("mida_total", "Desconeguda")
                fitxers = sec.get("fitxers", "Desconegut")
                barometre = sec.get("barometre", "Sense dades")

                arch_encontrados.insert(tk.END, f"{nom}\n")
                arch_encontrados.insert(tk.END, f"  Ruta       : {ruta}\n")
                arch_encontrados.insert(tk.END, f"  Mida total : {mida}\n")
                arch_encontrados.insert(tk.END, f"  Fitxers    : {fitxers}\n")
                arch_encontrados.insert(tk.END, f"  Baròmetre  : {barometre}\n")
                arch_encontrados.insert(tk.END, "----------------------------------------\n")

        arch_encontrados.see(tk.END)

    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo en: {LOG_FILE}")
    finally:
        # Reactivar botons quan acaba l’acció
        boton_iniciar.config(state="normal")
        btn_el.config(state="normal")
        btn_cons.config(state="normal")

def iniciar_carga():
    """
    Botó 'Iniciar Escaneo' -> analitza temporals (BAR_test1_TEMP.py via main.main()).
    """
    executar_accio_temp("ID2.1.1", lambda: main.main())

def aviso_eliminar():
    """
    Botó 'Eliminar' -> esborra temporals (DEL_test1_TEMP.py) i mostra el log igual.
    """
    arch_conservados.grid_forget()
    pregunta = messagebox.askquestion(
        'Eliminacion',
        'Los siguientes archivos seran eliminados.\n¿Está seguro?'
    )
    if pregunta == 'yes':
        try:
            btn_cons.config(state="disabled")
            executar_accio_temp("ID2.1.2", lambda: main.run_script("DEL_test1_TEMP.py"))
            arch_eliminados.grid(row=4, column=0, pady=5, sticky="w")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron eliminar los archivos. {e}")

def aviso_conservar():
    # Restablim la GUI de zero
    reset_gui()
    # Feedback visual
    arch_conservados.grid(row=4, column=0, pady=5, sticky="w")
    arch_eliminados.grid_forget()

# Títol columna esquerra
label_opciones = tk.Label(frame_botons, text="Opciones", bg="gray20", fg="white", font=("Arial", 11, "bold"))
label_opciones.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="w")

# Botó Iniciar (fila 1)
boton_iniciar = tk.Button(
    frame_botons,
    text="Iniciar Escaneo",
    command=iniciar_carga,
    font=("Arial", 12, "bold"),
    width=15
)
boton_iniciar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

# Botó Conservar (fila 2) – desactivat al principi
btn_cons = tk.Button(frame_botons, text="Conservar", command=aviso_conservar, width=15, state="disabled")
btn_cons.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")

# Botó Eliminar (fila 3) – desactivat al principi
btn_el = tk.Button(frame_botons, text="Eliminar", command=aviso_eliminar, width=15, state="disabled")
btn_el.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")

# Etiquetes d’estat (sota els botons, també a l’esquerra)
arch_eliminados = tk.Label(frame_botons, text='Archivos eliminados', font=("Arial", 11), bg="gray20", fg="red")
arch_conservados = tk.Label(frame_botons, text='Archivos conservados', font=("Arial", 11), bg="gray20", fg="green")

# Etiqueta "Resumen"
label_resumen = tk.Label(frame_requadres, text="Resumen", bg="gray20", fg="white", font=("Arial", 11, "bold"))
label_resumen.grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")

# 1r requadre: RESUM (dalt a la dreta)
arch_encontrados = tk.Text(frame_requadres, bg="#D3D3D3", height=8, width=60, font=("Arial", 11))
arch_encontrados.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

# Etiqueta "Todos los logs"
label_logs = tk.Label(frame_requadres, text="Todos los logs", bg="gray20", fg="white", font=("Arial", 11, "bold"))
label_logs.grid(row=2, column=0, padx=10, pady=(15, 0), sticky="w")

# 2n requadre: LOGS (baix a la dreta)
logs = tk.Text(frame_requadres, bg="#D3D3D3", height=8, width=60, font=("Arial", 11))
logs.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nsew")

window.mainloop()
