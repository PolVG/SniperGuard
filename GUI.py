import tkinter as tk
from PIL import Image, ImageTk
import time
from tkinter import ttk, messagebox
import main
from pathlib import Path
from datetime import datetime

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
boton1= Image.open("img/SniperGuardLogo.png")
NUEVO_ANCHO=70
NUEVO_ALTO=70
boton1_redimensionado = boton1.resize((NUEVO_ANCHO, NUEVO_ALTO), Image.LANCZOS)
imagen_del_boton = ImageTk.PhotoImage(boton1_redimensionado)
boton1_imagen_unico = tk.Button(barra_lateral,image=imagen_del_boton, bg="#9D9CA8",relief="flat",command=lambda: print("Home"))
boton1_imagen_unico.image = imagen_del_boton
boton1_imagen_unico.pack(pady=10, padx=10, fill='x')

#boton2
boton2 = Image.open("img/cleaner_sin_fondo.png")
NUEVO_ANCHO=70
NUEVO_ALTO=70
boton2_redimensionado = boton2.resize((NUEVO_ANCHO, NUEVO_ALTO), Image.LANCZOS)
imagen_del_boton = ImageTk.PhotoImage(boton2_redimensionado)
boton2_imagen_unico = tk.Button(barra_lateral,image=imagen_del_boton, bg="#9D9CA8",relief="flat",command=lambda: print("CLEANER clicked"))
boton2_imagen_unico.image = imagen_del_boton
boton2_imagen_unico.pack(pady=10, padx=10, fill='x')

#boton3
boton3 = Image.open("img/registry_sin_nombre.png")
NUEVO_ANCHO=70
NUEVO_ALTO=70
boton3_redimensionado = boton3.resize((NUEVO_ANCHO, NUEVO_ALTO), Image.LANCZOS)
imagen_del_boton = ImageTk.PhotoImage(boton3_redimensionado)
boton3_imagen_unico = tk.Button(barra_lateral,image=imagen_del_boton, bg="#9D9CA8",relief="flat",command=lambda: print("REGISTRY clicked"))
boton3_imagen_unico.image = imagen_del_boton
boton3_imagen_unico.pack(pady=10, padx=10, fill='x')

#boton4
boton4 = Image.open("img/herramientas_sin_fondo.png")
NUEVO_ANCHO=70
NUEVO_ALTO=70
boton4_redimensionado = boton3.resize((NUEVO_ANCHO, NUEVO_ALTO), Image.LANCZOS)
imagen_del_boton = ImageTk.PhotoImage(boton3_redimensionado)
boton4_imagen_unico = tk.Button(barra_lateral,image=imagen_del_boton, bg="#9D9CA8",relief="flat",command=lambda: print("HERRAMIENTAS clicked"))
boton4_imagen_unico.image = imagen_del_boton
boton4_imagen_unico.pack(pady=10, padx=10, fill='x')

#boton5
boton5 = Image.open("img/opciones_sin_fondo.png")
NUEVO_ANCHO=70
NUEVO_ALTO=70
boton5_redimensionado = boton5.resize((NUEVO_ANCHO, NUEVO_ALTO), Image.LANCZOS)
imagen_del_boton = ImageTk.PhotoImage(boton5_redimensionado)
boton4_imagen_unico = tk.Button(barra_lateral,image=imagen_del_boton, bg="#9D9CA8",relief="flat",command=lambda: print("OPCIONES clicked"))
boton4_imagen_unico.image = imagen_del_boton
boton4_imagen_unico.pack(pady=10, padx=10, fill='x')

''''
# Funcion para evitar codigo repetido para cada boton
def crear_boton(ruta, texto_log, fila):
    img = Image.open(ruta).resize((70, 70), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    btn = tk.Button(barra_lateral, image=img_tk, bg="#9D9CA8", relief="flat", command=lambda: print(texto_log))
    btn.image = img_tk
    btn.grid(row=fila, column=0, pady=10, padx=40, sticky='ew')
    return btn

crear_boton("img/SniperGuardLogo.png", "Home", 0)
crear_boton("img/cleaner_sin_fondo.png", "CLEANER clicked", 1)
crear_boton("img/registry_sin_nombre.png", "REGISTRY clicked", 2)
crear_boton("img/herramientas_sin_fondo.png", "HERRAMIENTAS clicked", 3)
crear_boton("img/opciones_sin_fondo.png", "OPCIONES clicked", 4)

'''
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

label_porcentaje = tk.Label(contenedor_principal, text="0%", bg="gray20", fg="#9D9CA8", font=("Impact", 15, "bold"))
label_porcentaje.grid(row=1, column=0, pady=5)

#funcion falseada para la barra de progreso
def iniciar_carga():
    # Ejecuta la lógica principal
    main.main()
    
    # Limpiar el cuadro de texto antes de empezar
    arch_encontrados.delete('1.0', tk.END)
    
    # Configuración de rutas
    BASE_DIR = Path(__file__).resolve().parent       
    PROJECT_ROOT = BASE_DIR.parent                     
    LOGS_DIR = PROJECT_ROOT / "logs"
    # Usamos el archivo específico que mencionaste
    LOG_FILE = LOGS_DIR /(datetime.now().strftime("%Y-%m-%d")+ "_logs_py.txt")

    try:
        with open(LOG_FILE, "r",encoding="utf-8") as f:
            lineas = f.readlines()
            total = len(lineas)
            
            if total == 0:
                arch_encontrados.insert(tk.END, "Archivo vacío.")
                return

            for i, linea in enumerate(lineas):
                # Actualizar barra de progreso y porcentaje
                porcentaje_actual = int(((i + 1) / total) * 100)
                progreso['value'] = porcentaje_actual
                label_porcentaje.config(text=f"{porcentaje_actual}%")
                
                # Insertar línea en el widget Text
                arch_encontrados.insert(tk.END, linea)
                arch_encontrados.see(tk.END) # Scroll automático
                
                # Refrescar interfaz y esperar 1 segundo
                window.update()
                time.sleep(0.1)
                
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo en: {LOG_FILE}")
    
boton_iniciar = tk.Button(contenedor_principal, text="Iniciar Escaneo", command=iniciar_carga, font=("Arial", 12, "bold"))
boton_iniciar.grid(row=2, column=0, pady=10)


arch_encontrados = tk.Text(contenedor_principal, bg="#D3D3D3", height=8, width=60, font=("Arial", 11))
arch_encontrados.grid(row=3, column=0, pady=10)


frame_botones_accion = tk.Frame(contenedor_principal, bg="gray20")
frame_botones_accion.grid(row=4, column=0, pady=5)

arch_eliminados = tk.Label(contenedor_principal, text='Archivos eliminados', font=("Arial", 11), bg="gray20", fg="red")
arch_conservados = tk.Label(contenedor_principal, text='Archivos conservados', font=("Arial", 11), bg="gray20", fg="green")

def aviso_eliminar():
    arch_conservados.grid_forget()
    pregunta = messagebox.askquestion('Eliminacion', 'Los siguientes archivos seran eliminados. \nEsta seguro ?')
    if pregunta == 'yes':
        arch_eliminados.grid(row=6, column=0, pady=5)

def aviso_conservar():
    arch_conservados.grid(row=6, column=0, pady=5)
    arch_eliminados.grid_forget()

btn_el = tk.Button(frame_botones_accion, text="Eliminar", command=aviso_eliminar, width=15)
btn_el.grid(row=0, column=0, padx=10)

btn_cons = tk.Button(frame_botones_accion, text="Conservar", command=aviso_conservar, width=15)
btn_cons.grid(row=0, column=1, padx=10)

logs = tk.Text(contenedor_principal, bg="#D3D3D3", height=8, width=60, font=("Arial", 11))
logs.grid(row=5, column=0, pady=10)

window.mainloop()





'''
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("SniperGuard - Alpha GUI")
root.geometry("500x520")
#root.resizable(False, False)  # desactiva el redimensionament (amplada, alçada)
root.configure(bg="#1e1e1e")  # fons de la finestra

# Configuració de la graella
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)

logo = tk.Label(root, text='SNIPERGUARD', font=("Arial", 20), bg="#1e1e1e", fg="white")
logo.grid(row=1, column=1, columnspan = 2, pady=10)

#Boton para el analisis simple
boton_analisis_rapido = tk.Button(root, text = "Anàlisi Ràpid",height=2, width=20, bg="#2980b9", fg="black", activebackground="#3498db", borderwidth=0)

#Display de logs
logs = tk.Text(root, bg = "#D3D3D3", height = 10, width = 50, font=("Arial", 13))
logs.grid(row=4, column=1, columnspan = 2)

#Display de archivos encontrados
arch_encontrados = tk.Text(root, bg = "#D3D3D3", height = 10, width = 50, font=("Arial", 13))
arch_encontrados.grid(row=2, column=1, columnspan = 2)

#Etiqueta archivos eliminados
arch_eliminados = tk.Label(root, text='Archivos eliminados', font=("Arial", 13))

#Etiqueta archivos conservados
arch_conservados = tk.Label(root, text='Archivos conservados', font=("Arial", 13))


def aviso_eliminar():
    arch_conservados.grid_forget()
    pregunta = messagebox.askquestion('Eliminacion', 'Los siguientes archivos seran eliminados. \nEsta seguro ?')
    if pregunta == 'yes':
        arch_eliminados.grid(row=5, column=1, columnspan = 2)

def aviso_conservar():
    arch_conservados.grid(row=5, column=1, columnspan = 2)
    arch_eliminados.grid_forget()
    
boton_analisis_rapido.grid(row=2, column=1, columnspan = 2, pady=30)
btn_el = tk.Button(root, text = "Eliminar", command = aviso_eliminar)
btn_el.grid(row=3, column=1, pady=10)
btn_cons = tk.Button(root, text = "Conservar", command = aviso_conservar)
btn_cons.grid(row=3, column=2, pady=10)






root.mainloop()
'''