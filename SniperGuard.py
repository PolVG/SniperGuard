import tkinter as tk
import random
import math

def iniciar_escaner(event=None):
    print("Iniciando escaneo...")
    canvas_boton.move(todo_el_boton, 0, 4)
    ventana.after(150, lambda: canvas_boton.move(todo_el_boton, 0, -4))

def abrir_terminos(event):
    ventana_terms = tk.Toplevel(ventana)
    ventana_terms.title("Terminos de Uso - Licencia MIT")
    ventana_terms.geometry("400x350")
    ventana_terms.configure(bg="#4b5320")
    ventana_terms.resizable(False, False)

    texto_licencia = """                      MIT License

Copyright (c) 2025 Sniper Guard Team

Por la presente, se concede permiso gratuito a cualquier persona que obtenga una copia de este software y los archivos de documentacion asociados (el Software) para utilizarlo sin restricciones.

El software se proporciona tal cual, sin garantia de ningun tipo.

"""

    frame_texto = tk.Frame(ventana_terms, bg="#4b5320")
    frame_texto.pack(fill="both", expand=True, padx=20, pady=20)

    texto_widget = tk.Text(
        frame_texto,
        wrap="word",
        bg="#4b5320",
        fg="#e6e6c8",
        font=("Courier", 9),
        relief="flat",
        borderwidth=0
    )
    texto_widget.pack(fill="both", expand=True)
    texto_widget.insert("1.0", texto_licencia)
    texto_widget.config(state="disabled")



def dibuixar_camuflat(canvas, ample, alt):
    colors = [
        "#6b8f4e",  # verd oliva
        "#556b2f",  # verd fosc
        "#8b5a2b",  # marron
        "#c2b280"   # beix
    ]

    for _ in range(120):
        cx = random.randint(0, ample)
        cy = random.randint(0, alt)
        radi = random.randint(20, 80)
        punts = random.randint(6, 12)
        color = random.choice(colors)

        coords = []
        for i in range(punts):
            angle = 2 * math.pi * i / punts
            variacio = random.uniform(0.6, 1.2)
            x = cx + math.cos(angle) * radi * variacio
            y = cy + math.sin(angle) * radi * variacio
            coords.extend([x, y])

        canvas.create_polygon(
            coords,
            fill=color,
            outline=""
        )

def entrar_raton(event):
    canvas_boton.config(cursor="hand2")
    canvas_boton.itemconfig(circulo_principal, fill="#6b8e23")

def salir_raton(event):
    canvas_boton.itemconfig(circulo_principal, fill="#556b2f")

def entrar_enlace(event):
    terminos_uso.config(fg="#c2c28c", cursor="hand2")

def salir_enlace(event):
    terminos_uso.config(fg="#a0a070")

# Configuracion principal
ventana = tk.Tk()
ventana.title("Sniper Guard")
ventana.geometry("600x450")
ventana.configure(bg="#4b5320")

# Barra lateral (SIN CAMBIOS)
barra_lateral = tk.Frame(ventana, bg="#2c3e50", width=65)
barra_lateral.pack(side="left", fill="y")
barra_lateral.pack_propagate(False)

# Area principal
area_principal = tk.Frame(ventana, bg="#4b5320")
area_principal.pack(side="right", expand=True, fill="both")

# Canvas de fondo con camuflaje
canvas_fondo = tk.Canvas(
    area_principal,
    bg="#4b5320",
    highlightthickness=0
)
canvas_fondo.place(relwidth=1, relheight=1)

# Dibujar manchas marrones
for _ in range(18):
    x = random.randint(0, 600)
    y = random.randint(0, 450)
    r = random.randint(30, 80)
    canvas_fondo.create_oval(
        x - r, y - r, x + r, y + r,
        fill="#6b4f1d",
        outline=""
    )

alpha_label = tk.Label(
    area_principal,
    text="Alpha: software en construccion",
    font=("Arial", 10, "bold"),
    fg="#d4aa00",
    bg="#4b5320"
)
alpha_label.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

terminos_uso = tk.Label(
    area_principal,
    text="Terminos de uso | Politica de Privacidad | V.1.0",
    bg="#4b5320",
    fg="#a0a070",
    font=("Arial", 8, "underline")
)
terminos_uso.pack(side="bottom", pady=(0, 20))
terminos_uso.bind("<Button-1>", abrir_terminos)
terminos_uso.bind("<Enter>", entrar_enlace)
terminos_uso.bind("<Leave>", salir_enlace)

contenedor_centro = tk.Frame(area_principal, bg="#4b5320")
contenedor_centro.pack(expand=True)

titulo = tk.Label(
    contenedor_centro,
    text="SNIPER GUARD",
    font=("Segoe UI", 28, "bold"),
    bg="#4b5320",
    fg="#d6d6aa"
)
titulo.pack(pady=(0, 50))

canvas_boton = tk.Canvas(
    contenedor_centro,
    width=160,
    height=170,
    bg="#4b5320",
    highlightthickness=0
)
canvas_boton.pack()

x0, y0 = 10, 10
x1, y1 = 150, 150

sombra = canvas_boton.create_oval(
    x0, y0 + 8, x1, y1 + 8,
    fill="#3e2f14",
    outline=""
)

circulo_principal = canvas_boton.create_oval(
    x0, y0, x1, y1,
    fill="#556b2f",
    outline=""
)

texto = canvas_boton.create_text(
    80, 80,
    text="Clean",
    font=("Segoe UI", 24, "bold"),
    fill="white"
)

canvas_boton.addtag_all("todo_el_boton")
todo_el_boton = "todo_el_boton"

canvas_boton.tag_bind(circulo_principal, "<Button-1>", iniciar_escaner)
canvas_boton.tag_bind(texto, "<Button-1>", iniciar_escaner)
canvas_boton.tag_bind(circulo_principal, "<Enter>", entrar_raton)
canvas_boton.tag_bind(texto, "<Enter>", entrar_raton)
canvas_boton.tag_bind(circulo_principal, "<Leave>", salir_raton)
canvas_boton.tag_bind(texto, "<Leave>", salir_raton)

ventana.mainloop()
