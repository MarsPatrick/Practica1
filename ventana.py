from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import uuid


# Tomar  Foto Total (360)
def tft():
    print("Lo que hara")


# Tomar Foto
def tf():
    leido, frame = cap.read()
    if leido:
        nombre_foto = str(uuid.uuid4()) + ".png"
        cv2.imwrite(nombre_foto, frame)
        print("Foto tomada correctamente")
    else:
        print("Error al acceder a la cámara")


def iniciar():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if cap is None or not cap.isOpened():
        btn0['state'] = NORMAL
        btn1['state'] = DISABLED
        btn2['state'] = DISABLED
        btn3['state'] = DISABLED
        lblimg.grid(column=0, row=0, columnspan=2)
        messagebox.showerror("ERROR", "NO HAY CAMARA")
    else:
        btn0['state'] = DISABLED
        btn1['state'] = NORMAL
        btn2['state'] = NORMAL
        btn3['state'] = NORMAL
        lblimg.grid_forget()
        visualizar()


def visualizar():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            toy = objetoClassif.detectMultiScale(gray, scaleFactor=5, minNeighbors=91, minSize=(70, 78))

            for (x, y, w, h) in toy:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, 'Audifono', (x, y - 10), 2, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
        else:
            lblVideo.image = ""
            finalizar()


def finalizar():
    global cap
    cap.release()
    lblimg.grid(column=0, row=0, columnspan=2)
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
btn0 = Button(left_frame, text='Ver previa', padx=12, pady=105, command=iniciar)
btn0.grid(column=0, row=0, padx=5, pady=5)

# Button 1
btn1 = Button(left_frame, text='Ocultar previa', pady=105, command=finalizar, state=DISABLED)
btn1.grid(column=0, row=1, padx=5, pady=5)

# Button 2
btn2 = Button(right_frame, text='Tomar foto', padx=11, pady=113, command=tf, state=DISABLED)
btn2.grid(column=0, row=0, padx=5, pady=5)

# Button 3
btn3 = Button(right_frame, text='Tomar foto 360', pady=113, command=tft, state=DISABLED)
btn3.grid(column=0, row=1, padx=5, pady=5)

# Video
lblVideo = Label(mid_frame)
lblVideo.grid(column=0, row=0, columnspan=2)

img = Image.open('x.gif')
imgn = ImageTk.PhotoImage(img)
lblimg = Label(mid_frame, image=imgn)
lblimg.grid(column=0, row=0, columnspan=2)

# A implementar cuando exista mas de una camara
combo = ttk.Combobox(left_frame, state="disabled", width=10)
combo["values"] = ["Python", "C", "C++", "Java"]
combo.grid(column=0, row=2, padx=5, pady=5)
objetoClassif = cv2.CascadeClassifier('cascade.xml')
ventana.mainloop()
