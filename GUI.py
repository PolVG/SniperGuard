import tkinter as tk

root = tk.Tk()
root.title("SniperGuard - Alpha GUI")
root.geometry("500x400")
root.resizable(False, False)  # desactiva el redimensionament (amplada, alçada)
root.configure(bg="#1e1e1e")  # fons de la finestra

# Configuració de la graella
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)


logs = tk.Label(root, text='SNIPERGUARD', font=("Arial", 20), bg="#1e1e1e", fg="white")
logs.grid(row=1, column=1, pady=10)





boton_analisis_rapido = tk.Button(root, text = "Anàlisi Ràpid",height=2, width=20, bg="#2980b9", fg="black", activebackground="#3498db", borderwidth=0)
boton_analisis_rapido.grid(row=2, column=1,pady=30)


root.mainloop()