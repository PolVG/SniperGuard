import tkinter as tk

# Ventana principal
ventana = tk.Tk()
ventana.title("Sniper Guard")
ventana.geometry("500x400")
ventana.configure(bg="black")

# Barra lateral
tk.Frame(ventana, bg="#1a1a1a", width=60).pack(side="left", fill="y")

# Area principal
main = tk.Frame(ventana, bg="black")
main.pack(side="right", expand=True, fill="both", padx=40, pady=40)

# Titulo
tk.Label(main, text="SNIPER GUARD", font=("Arial", 28, "bold"), fg="red", bg="black").pack(pady=(20, 40))

# Boton circular
canvas_boton = tk.Canvas(main, width=140, height=140, bg="black", highlightthickness=0)
canvas_boton.pack()

# Dibujar boton (sombra, circulo, texto) (este apartado ha sido generado por IA)
canvas_boton.create_oval(10, 18, 130, 138, fill="#8b0000")  # Sombra
circulo = canvas_boton.create_oval(10, 10, 130, 130, fill="red")  # Boton
canvas_boton.create_text(70, 70, text="Clean", font=("Arial", 22, "bold"), fill="white")

# Funcion para el boton
def clic_boton(event):
    canvas_boton.move("all", 0, 4)  
    ventana.after(100, lambda: canvas_boton.move("all", 0, -4)) 

# Funcion para mostrar licencia
def mostrar_licencia():
    nueva_ventana = tk.Toplevel(ventana)
    nueva_ventana.title("Terminos y Politica")
    nueva_ventana.geometry("500x350")
    nueva_ventana.configure(bg="black")
    
    texto_licencia = """MIT License

    Copyright (c) 2025 Sniper Guard Team

Por la presente, se concede permiso gratuito a cualquier persona que obtenga una copia de este software y los archivos de documentacion asociados (el Software) para utilizarlo sin restricciones.

El software se proporciona tal cual, sin garantia de ningun tipo."""
    
    tk.Label(nueva_ventana, text=texto_licencia, justify="left", font=("Courier", 10),
            fg="red", bg="black", wraplength=450, padx=20, pady=20).pack(anchor="w")

# Funciones para efectos del boton
def raton_entra_boton(event):
    canvas_boton.config(cursor="hand2")
    canvas_boton.itemconfig(circulo, fill="#ff4444")

def raton_sale_boton(event):
    canvas_boton.itemconfig(circulo, fill="red")

# Conectar eventos al boton
canvas_boton.bind("<Button-1>", clic_boton)
canvas_boton.bind("<Enter>", raton_entra_boton)
canvas_boton.bind("<Leave>", raton_sale_boton)

# Crear enlace inferior
enlace_inferior = tk.Label(main, text="Terminos de uso | Politica de Privacidad | V.2.0", 
                          fg="red", bg="black", font=("Arial", 9), cursor="hand2", pady=20)
enlace_inferior.pack(side="bottom")

# Funciones para efectos del enlace
def raton_entra_enlace(event):
    enlace_inferior.config(fg="#ff4444")

def raton_sale_enlace(event):
    enlace_inferior.config(fg="red")

# Conectar eventos al enlace
enlace_inferior.bind("<Enter>", raton_entra_enlace)
enlace_inferior.bind("<Leave>", raton_sale_enlace)
enlace_inferior.bind("<Button-1>", lambda e: mostrar_licencia())

# Iniciarlo
ventana.mainloop()

