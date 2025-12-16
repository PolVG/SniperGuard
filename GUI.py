import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Aviso")
root.geometry("800x200")


logs = tk.Label(root, text='Logs', font=("Arial", 13))
logs.grid(row=1, column=1)

arch_encontrados = tk.Label(root, text='Archivos encontrados', font=("Arial", 13))
arch_encontrados.grid(row=1, column=2)

arch_eliminados = tk.Label(root, text='Archivos eliminados', font=("Arial", 13))

arch_conservados = tk.Label(root, text='Archivos conservados', font=("Arial", 13))

def aviso_eliminar():
    arch_eliminados.grid(row=3, column=1, columnspan = 2)
    arch_conservados.grid_forget()

def aviso_conservar():
    arch_conservados.grid(row=3, column=1, columnspan = 2)
    arch_eliminados.grid_forget()
    

btn_el = tk.Button(root, text = "Eliminar", command = aviso_eliminar)
btn_el.grid(row=2, column=1)
btn_cons = tk.Button(root, text = "Conservar", command = aviso_conservar)
btn_cons.grid(row=2, column=2)

root.mainloop()