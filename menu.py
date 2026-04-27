import tkinter as tk
import subprocess
import sys
import os

def lanzar_juego(nombre_archivo):
    # Obtener la ruta absoluta del directorio actual
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_juego = os.path.join(directorio_actual, nombre_archivo)
    
    # Ejecutar el script de Python seleccionado
    # sys.executable asegura que se use el mismo intérprete de Python
    subprocess.Popen([sys.executable, ruta_juego])

def jugar_espejo():
    lanzar_juego('espejo.py')

def jugar_flappy():
    lanzar_juego('flappy.py')

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Menú de Videojuegos")
ventana.geometry("350x250")
ventana.configure(bg="#2c3e50") # Color de fondo elegante

# Título del menú
titulo = tk.Label(ventana, text="Selecciona tu Aventura", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="white")
titulo.pack(pady=20)

# Botón para el Cazador de Monstruos Mágico (espejo.py)
btn_espejo = tk.Button(ventana, text="🎮 Cazador de Monstruos", 
                       font=("Helvetica", 12), 
                       bg="#3498db", fg="white", 
                       activebackground="#2980b9", activeforeground="white",
                       width=25, height=2,
                       command=jugar_espejo)
btn_espejo.pack(pady=10)

# Botón para Flappy Pygame (flappy.py)
btn_flappy = tk.Button(ventana, text="🐦 Flappy Pygame", 
                       font=("Helvetica", 12), 
                       bg="#2ecc71", fg="white", 
                       activebackground="#27ae60", activeforeground="white",
                       width=25, height=2,
                       command=jugar_flappy)
btn_flappy.pack(pady=10)

# Iniciar el bucle de la aplicación
ventana.mainloop()