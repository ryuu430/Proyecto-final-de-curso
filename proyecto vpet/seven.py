# Crearo por Izan

import random
import tkinter as tk
import ctypes

# Ruta de sprites (importante cambiar por vuestra ruta)
ruta_imagenes = r'F:\2 curso\pagina web\Proyecto_python\proyecto vpet\sprites_seven\\'

# Obtener resolución de la pantalla
user32 = ctypes.windll.user32
ancho_pantalla = user32.GetSystemMetrics(0)
alto_pantalla = user32.GetSystemMetrics(1)

# Posición inicial de la mascota
pos_x = int(ancho_pantalla * 0.7)
pos_y = int(alto_pantalla * 0.85)

ciclo = 0
estado = 1  # estado de animación

numeros_idle = [1, 2, 3, 4]
numeros_dormir = [10, 11, 12, 13, 15]
numeros_caminar_izq = [6, 7]
numeros_caminar_der = [8, 9]

numero_evento = random.randint(1, 3)




# Eventos
def evento(ciclo, estado, numero_evento, pos_x):
    if numero_evento in numeros_idle:
        estado = 0
        ventana.after(300, actualizar, ciclo, estado, numero_evento, pos_x)

    elif numero_evento == 5:
        estado = 1
        ventana.after(100, actualizar, ciclo, estado, numero_evento, pos_x)

    elif numero_evento in numeros_caminar_izq:
        estado = 4
        ventana.after(100, actualizar, ciclo, estado, numero_evento, pos_x)

    elif numero_evento in numeros_caminar_der:
        estado = 5
        ventana.after(100, actualizar, ciclo, estado, numero_evento, pos_x)

    elif numero_evento in numeros_dormir:
        estado = 2
        ventana.after(1000, actualizar, ciclo, estado, numero_evento, pos_x)

    elif numero_evento == 14:
        estado = 3
        ventana.after(100, actualizar, ciclo, estado, numero_evento, pos_x)



# Avanca el fotograma del gif
def avanzar_gif(ciclo, fotogramas, numero_evento, inicio, fin):
    if ciclo < len(fotogramas) - 1:
        ciclo += 1
    else:
        ciclo = 0
        numero_evento = random.randint(inicio, fin)
    return ciclo, numero_evento



# Se actualiza la animación
def actualizar(ciclo, estado, numero_evento, pos_x):
    global pos_y

    if estado == 0:  # idle
        fotograma = idle[ciclo]
        ciclo, numero_evento = avanzar_gif(ciclo, idle, numero_evento, 1, 9)

    elif estado == 1:  # idle → dormir
        fotograma = idle_a_dormir[ciclo]
        ciclo, numero_evento = avanzar_gif(ciclo, idle_a_dormir, numero_evento, 10, 10)

    elif estado == 2:  # dormir
        fotograma = dormir[ciclo]
        ciclo, numero_evento = avanzar_gif(ciclo, dormir, numero_evento, 10, 15)

    elif estado == 3:  # dormir → idle
        fotograma = dormir_a_idle[ciclo]
        ciclo, numero_evento = avanzar_gif(ciclo, dormir_a_idle, numero_evento, 1, 1)

    elif estado == 4:  # caminar izquierda
        fotograma = caminar_izq[ciclo]
        ciclo, numero_evento = avanzar_gif(ciclo, caminar_izq, numero_evento, 1, 9)
        pos_x -= 3

    elif estado == 5:  # caminar derecha
        fotograma = caminar_der[ciclo]
        ciclo, numero_evento = avanzar_gif(ciclo, caminar_der, numero_evento, 1, 9)
        pos_x += 3

    # Evitar que salga de la pantalla
    pos_x = max(0, min(pos_x, ancho_pantalla - 100))

    ancho = fotograma.width()
    alto = fotograma.height()
    ventana.geometry(f'{ancho}x{alto}+{pos_x}+{pos_y}')

    etiqueta.configure(image=fotograma)

    ventana.after(1, evento, ciclo, estado, numero_evento, pos_x)



# Configuracion de tkinter
ventana = tk.Tk()
ventana.attributes("-topmost", True) # al frente

idle = [tk.PhotoImage(file=ruta_imagenes + 'idle.gif', format='gif -index %i' % i) for i in range(7)]
idle_a_dormir = [tk.PhotoImage(file=ruta_imagenes + 'idle_to_sleep.gif', format='gif -index %i' % i) for i in range(3)]
dormir = [tk.PhotoImage(file=ruta_imagenes + 'sleep.gif', format='gif -index %i' % i) for i in range(9)]
dormir_a_idle = [tk.PhotoImage(file=ruta_imagenes + 'sleep_to_idle.gif', format='gif -index %i' % i) for i in range(3)]
caminar_izq = [tk.PhotoImage(file=ruta_imagenes + 'walking_positive.gif', format='gif -index %i' % i) for i in range(3)]
caminar_der = [tk.PhotoImage(file=ruta_imagenes + 'walking_negative.gif', format='gif -index %i' % i) for i in range(3)]

ventana.config(highlightbackground='black')
etiqueta = tk.Label(ventana, bd=0, bg='black')
ventana.overrideredirect(True)
ventana.wm_attributes('-transparentcolor', 'black')
etiqueta.pack()

# Click derecho sobre la mascota para salir
def cerrar(evento):
    ventana.destroy()

ventana.bind("<Button-3>", cerrar)


# Inicia y se mantiene activo hasta que se pare
ventana.after(1, actualizar, ciclo, estado, numero_evento, pos_x)
ventana.mainloop()
