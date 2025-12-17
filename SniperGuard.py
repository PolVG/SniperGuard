import tkinter as tk

def iniciar_escaner(event=None): 
    print("Iniciando escaneo...")
    # Animacion al pulsar"
    canvas_boton.move(todo_el_boton, 0, 4) # Bajar
    ventana.after(150, lambda: canvas_boton.move(todo_el_boton, 0, -4)) # Subir

# Funcion ventana de termino
def abrir_terminos(event):
    ventana_terms = tk.Toplevel(ventana)
    ventana_terms.title("Terminos de Uso - Licencia MIT")
    ventana_terms.geometry("400x350")
    ventana_terms.configure(bg="white")
    ventana_terms.resizable(False, False)
    
    texto_licencia = """    MIT License
    Copyright (c) 2025 Sniper Guard Team

Por la presente, se concede permiso gratuito a cualquier persona que obtenga una copia de este software y los archivos de documentacion asociados (el Software) para utilizarlo sin restricciones.

El software se proporciona tal cual, sin garantia de ningun tipo

    """
    
    frame_texto = tk.Frame(ventana_terms, bg="white")
    frame_texto.pack(fill="both", expand=True, padx=20, pady=20)
    
    texto_widget = tk.Text(frame_texto, wrap="word", bg="white", font=("Courier", 9), padx=10, pady=10, height=12, width=45, relief="flat", borderwidth=0)
    texto_widget.pack(fill="both", expand=True)
    texto_widget.insert("1.0", texto_licencia)
    texto_widget.config(state="disabled")

# Funciones visuales
def entrar_raton(event):
    canvas_boton.config(cursor="hand2") 
    # Hacemos el azul un poco más claro al pasar el ratón
    canvas_boton.itemconfig(circulo_principal, fill="#4dabf5") 

def salir_raton(event):
    # Volvemos al azul original
    canvas_boton.itemconfig(circulo_principal, fill="#2196F3") 

def entrar_enlace(event):
    terminos_uso.config(fg="#3498db", cursor="hand2")

def salir_enlace(event):
    terminos_uso.config(fg="#999")

# Configuracion principal
ventana = tk.Tk()
ventana.title("Sniper Guard")
ventana.geometry("600x450")
ventana.configure(bg="#f0f0f0") 

# Barra lateral
barra_lateral = tk.Frame(ventana, bg="#2c3e50", width=65)
barra_lateral.pack(side="left", fill="y")
barra_lateral.pack_propagate(False)

# Area principal
area_principal = tk.Frame(ventana, bg="#f0f0f0")
area_principal.pack(side="right", expand=True, fill="both")

alpha_label = tk.Label(area_principal, text="Alpha: software en construccion", font=("Arial", 10, "bold"), fg="#ff8c00", bg="#f0f0f0", padx=10, pady=5)
alpha_label.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

terminos_uso = tk.Label(area_principal, text="Terminos de uso | Politica de Privacidad | V.1.0", bg="#f0f0f0", fg="#999", font=("Arial", 8, "underline"))
terminos_uso.pack(side="bottom", pady=(0, 20))
terminos_uso.bind("<Button-1>", abrir_terminos)
terminos_uso.bind("<Enter>", entrar_enlace)
terminos_uso.bind("<Leave>", salir_enlace)

contenedor_centro = tk.Frame(area_principal, bg="#f0f0f0")
contenedor_centro.pack(expand=True)

titulo = tk.Label(contenedor_centro, text="SNIPER GUARD", font=("Segoe UI", 28, "bold"), bg="#f0f0f0", fg="#3498db")
titulo.pack(pady=(0, 50)) 

# Boton dibujado
canvas_boton = tk.Canvas(contenedor_centro, width=160, height=170, bg="#f0f0f0", highlightthickness=0)
canvas_boton.pack()

# Coordenadas del botón
x0, y0 = 10, 10
x1, y1 = 150, 150

# Hacerle sombra al boton
sombra = canvas_boton.create_oval(x0, y0+8, x1, y1+8, fill="#1565c0", outline="")

# Boton principal
circulo_principal = canvas_boton.create_oval(x0, y0, x1, y1, fill="#2196F3", outline="")

# Texto del boton
texto = canvas_boton.create_text(80, 80, text="Clean", font=("Segoe UI", 24, "bold"), fill="white")

# Agrupar todo para moverlo junto (usando un tag 'boton')
canvas_boton.addtag_all("todo_el_boton")
todo_el_boton = "todo_el_boton"

# Eventos
canvas_boton.tag_bind(circulo_principal, "<Button-1>", iniciar_escaner)
canvas_boton.tag_bind(texto, "<Button-1>", iniciar_escaner)
canvas_boton.tag_bind(circulo_principal, "<Enter>", entrar_raton)
canvas_boton.tag_bind(texto, "<Enter>", entrar_raton)
canvas_boton.tag_bind(circulo_principal, "<Leave>", salir_raton)
canvas_boton.tag_bind(texto, "<Leave>", salir_raton)

ventana.mainloop()