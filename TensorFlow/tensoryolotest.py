import cv2
import numpy as np
import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage

#   Declaracion de variables globales para ocupar mas adelante
global Directorio, cont, cap, nombre, text
Directorio = os.getcwd()
text = ""
cont = 1

#   Esta variable debe ser igual a la del yolov3.cfg
#   Normalmente en la Linea 8 y 9 aparece width y height
#   los valores debiesen ser iguales entre si
#   Anotar ese valor en esta variable
#   Variable modificable segun el cfg
whT = 608

#   confThreshold va de 0 a 1 sin ocupar el ultimo
#   se ocupa para decir que tan preciso debe ser el detector
#   donde 0 es 0% y 1 es 100%
#   Variable modificable segun el usuario
confThreshold = 0.5

#   nmsThreshold va de 0 a 1 sin ocupar el ultimo
#   se ocupa para decir que tan agresivo debe ser el detector
#   mientras menos valor tenga, mas agresivo sera el detector
#   Variable modificable segun el usuario
nmsThreshold = 0.3

#   Lectura de los nombres de los objetos en el modelo entrenado
#   Variable modificable segun el archivo de nombres
classesFile = 'coco.names'

classNames = []
with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

#   Lectura de la configuracion y la red neuronal
#   Variables modificables segun su nombre de archivo
modelConfiguration = 'yolov3.cfg'
modelWeights = 'yolov3.weights'

#Iniciar la red neuronal
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
#   Teoricamente se puede usar CUDA para usar tarjeta grafica en vez de cpu
#   De momento no se ha testeado
#net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

#   Esta funcion recibe las capas que se encuentran en camara
#   con esto, busca el porcentaje de aproximacion mas alta
#   y devuelve el nombre con el porcentaje del objeto reconocido
def findObjects(outputs, img):
    global nombre
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))
    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
    nom = " "
    for i in indices:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%',
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        nom = classNames[classIds[i]].upper()
    nombre=nom

class ventanaui(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.btn0.clicked.connect(self.activar)
        self.btn0.clicked.connect(self.viewCam)
        self.btn1.clicked.connect(self.desactivar)
        self.btn2.clicked.connect(self.tomarfoto)
        self.btn4.clicked.connect(self.guardar_ruta)

    #   Agregarle funciones al boton que activa la camara
    def activar(self):
        global cap
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.btn0.setEnabled(False)
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(True)
        self.btn4.setEnabled(True)

    #   Agregarle funciones al boton que desactiva la camara
    def desactivar(self):
        self.btn0.setEnabled(True)
        self.btn1.setEnabled(False)
        self.btn2.setEnabled(False)
        self.btn4.setEnabled(False)
        global cap
        cap.release()
        self.lblVideo.setPixmap(QPixmap('x2.jpg'))

    def viewCam(self):
        while cap.isOpened():
            success, img = cap.read()
            if success:
                #   Aca empieza el reconocimiento
                #   En esta parte se empiezan a reconocer las imagenes por camara
                #   Estas las comopara con las capas de la red neuronal
                blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
                net.setInput(blob)
                layerNames = net.getLayerNames()
                outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
                outputs = net.forward(outputNames)
                #   Estas se mandan a la funcion para encontrar el objeto
                findObjects(outputs, img)
                self.displayImage(img)
                cv2.waitKey(1)
            else:
                self.activar()
                self.errorcamara()

    #   Funcion que da formato a la camara y muestra la imagen en vivo
    def displayImage(self, img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.lblVideo.setPixmap(QPixmap.fromImage(img))

    #   Funcion que arroja en caso de no encontrar una camara
    #   Esta funcion puede fallar debido que en cierta actualizacion de windows 10
    #   hubo un cambio y reconoce una camara falsa sin dar imagen alguna
    def errorcamara(self):
        QMessageBox.about(self, "ERROR", "NO SE PUEDE ACCEDER A LA CAMARA")

    #   Funcion para elegir la ruta donde se guardaran las fotos sacadas
    def guardar_ruta(self):
        global Directorio, cont
        dialog = QFileDialog()
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        dialog.setWindowTitle("Seleccionar donde guardar las fotos")
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QFileDialog.Accepted:
            Directorio = dialog.selectedFiles()[0]
        cont = 1

    #   En esta funcion se guarda la foto y la guarda en la ruta por defecto,
    #   la cual es donde se esta ocupando o la ruta elegida por el usuario
    #   y se guarda en una carpeta llamada FotoGuardada para mas comodidad
    def tomarfoto(self):
        global Directorio, cont, nombre, cap, text
        leido, frame = cap.read()
        if leido:
            if nombre == " ":
                #   Variable que le da nombre al objeto en caso de no
                #   reconocio ninguno el programa
                nombre = "objetonoreconocido"

            #   Variable que se puede borrar el + "\FotoGuardada"
            #   para guardarlo en la misma carpeta
            dire = Directorio + "\FotoGuardada"
            if not os.path.exists(dire):
                os.makedirs(dire)
            dire = dire + "\\" + nombre + str(cont) + ".jpg"
            if not cv2.imwrite(dire, frame):
                raise Exception("No se puede guardar la imagen en: "+dire)

            #   Se puede editar el texto a mostrar, no lo demas
            text = text + "Foto tomada correctamente y guardada en: " + dire
            self.textBrowser.setText(text)
            text = text + "\n"
            cont += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = ventanaui()
    GUI.show()
    sys.exit(app.exec_())
