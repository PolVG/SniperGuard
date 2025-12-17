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