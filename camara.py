from tkinter import messagebox
import cv2
import imutils
import uuid

# XML de los objetos
objetoClassif = cv2.CascadeClassifier('cascade.xml')


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
        desactivar()
        lblimg.grid(column=0, row=0, columnspan=2)
        messagebox.showerror("ERROR", "NO HAY CAMARA")
    else:
        activar()
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
    desactivar()


from layout import *

ventana.mainloop()
