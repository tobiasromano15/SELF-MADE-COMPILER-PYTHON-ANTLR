import tkinter as tk
from tkinter import filedialog

from main import main_function


def seleccionar_archivo_y_ejecutar():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        main_function(filepath)
        print(f"Archivo seleccionado: {filepath}")
        app.destroy()

app = tk.Tk()
app.geometry("600x400")
app.title("Ejecutar main.py")

btn = tk.Button(app, text="Seleccionar archivo .txt y ejecutar", command=seleccionar_archivo_y_ejecutar)
btn.pack(pady=20)

app.mainloop()
import tkinter as tk

def mostrar_contenido(archivo):
    try:
        with open(archivo, 'r') as f:
            contenido = f.read()
            texto.delete(1.0, tk.END)
            texto.insert(tk.END, contenido)
    except FileNotFoundError:
        texto.delete(1.0, tk.END)
        texto.insert(tk.END, "Archivo no encontrado.")

# Crear una ventana
ventana = tk.Tk()
ventana.title("Visualizador de Archivos de Texto")

# Crear un widget de texto para mostrar el contenido
texto = tk.Text(ventana)
texto.pack()

# Botones para mostrar los archivos
boton_errores = tk.Button(ventana, text="Mostrar Errores", command=lambda: mostrar_contenido("errores.txt"))
boton_errores.pack()

boton_salida = tk.Button(ventana, text="Mostrar Salida", command=lambda: mostrar_contenido("salida.txt"))
boton_salida.pack()

boton_tabla_simbolos = tk.Button(ventana, text="Mostrar Tabla de Símbolos", command=lambda: mostrar_contenido("tabla_de_simbolos.txt"))
boton_tabla_simbolos.pack()

# Iniciar la interfaz gráfica
ventana.mainloop()
