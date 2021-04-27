from tkinter import *
from PIL import Image
from PIL import ImageTk
from camara import *


def activar():
    btn0['state'] = DISABLED
    btn1['state'] = NORMAL
    btn2['state'] = NORMAL
    btn3['state'] = NORMAL


def desactivar():
    btn0['state'] = NORMAL
    btn1['state'] = DISABLED
    btn2['state'] = DISABLED
    btn3['state'] = DISABLED


# Ventana
# Creacion de Ventana
ventana = Tk()

# Tamaño de la ventana
ventana.geometry("870x530")

# Titulo de la ventana
ventana.title("Titulo")

# Creacion de Frames
left_frame = Frame(ventana, width=200, height=400, bg='grey')
left_frame.grid(row=0, column=0, padx=5, pady=5)

mid_frame = Frame(ventana)
mid_frame.grid(row=0, column=1, padx=5, pady=5)

right_frame = Frame(ventana, width=650, height=400, bg='grey')
right_frame.grid(row=0, column=2, padx=5, pady=5)

# Botones
# Button 0
btn0 = Button(left_frame, text='Ver previa', padx=12, pady=113, command=iniciar)
btn0.grid(column=0, row=0, padx=5, pady=5)

# Button 1
btn1 = Button(left_frame, text='Ocultar previa', pady=113, state=DISABLED, command=finalizar)
btn1.grid(column=0, row=1, padx=5, pady=5)

# Button 2
btn2 = Button(right_frame, text='Tomar foto', padx=11, pady=113, state=DISABLED, command=tf)
btn2.grid(column=0, row=0, padx=5, pady=5)

# Button 3
btn3 = Button(right_frame, text='Tomar foto 360', pady=113, state=DISABLED, command=tft)
btn3.grid(column=0, row=1, padx=5, pady=5)

# Video
lblVideo = Label(mid_frame)
lblVideo.grid(column=0, row=0, columnspan=2)

# Imagen de camara apagada
img = Image.open('x.gif')
imgn = ImageTk.PhotoImage(img)
lblimg = Label(mid_frame, image=imgn)
lblimg.grid(column=0, row=0, columnspan=2)
