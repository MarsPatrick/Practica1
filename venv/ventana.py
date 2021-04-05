from tkinter import *
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import cv2
import imutils

# Una accion generica
def accion():
    print("Lo que hara")



# VentanaEmergente(Info)
def vei():
    print("Lo que hara")

def iniciar():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    visualizar()

def visualizar():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
        else:
            lblVideo.image = ""
            cap.release()

def finalizar():
    global cap
    cap.release()


# Declaracion de la ventana
ventana = Tk()

# Create left and right frames
left_frame = Frame(ventana, width=200, height=400, bg='grey')
left_frame.grid(row=0, column=0, padx=10, pady=5)

mid_frame = Frame(ventana, width=650, height=400, bg='grey')
mid_frame.grid(row=0, column=1, padx=10, pady=5)

right_frame = Frame(ventana, width=650, height=400, bg='grey')
right_frame.grid(row=0, column=2, padx=10, pady=5)

# Tamaño de la ventana
ventana.geometry("900x500")

# Titulo de la ventana
ventana.title("Titulo")

# Button
btn0 = Button(left_frame, text='Ver previa', command=iniciar)
btn0.grid(column=0, row=0, padx=5, pady=5)

# Button
btn1 = Button(left_frame, text='Ocultar previa', command=finalizar)
btn1.grid(column=0, row=1, padx=5, pady=5)

# Button
btn2 = Button(right_frame, text='Tomar foto', command=vei)
btn2.grid(column=0, row=0, padx=5, pady=5)

# Button
btn3 = Button(right_frame, text='Tomar foto 360', command=vei)
btn3.grid(column=0, row=1, padx=5, pady=5)

# Video
lblVideo= Label(mid_frame)
lblVideo.grid(column=0, row=0, columnspan=2)

ventana.mainloop()