import cv2
import numpy as np
import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage

global Directorio, cont, cap, nombre, text
Directorio = os.getcwd()
text = ""
cont = 1

whT = 416
confThreshold = 0.5
nmsThreshold = 0.3

classesFile = 'coco.names'
classNames = []
with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
modelConfiguration = 'yolov3.cfg'
modelWeights = 'yolov3.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


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

    def activar(self):
        global cap
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.btn0.setEnabled(False)
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(True)
        self.btn4.setEnabled(True)

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
                blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
                net.setInput(blob)
                layerNames = net.getLayerNames()
                outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
                outputs = net.forward(outputNames)
                findObjects(outputs, img)
                self.displayImage(img)
                cv2.waitKey(1)
            else:
                self.activar()
                self.errorcamara()

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

    def errorcamara(self):
        QMessageBox.about(self, "ERROR", "NO SE PUEDE ACCEDER A LA CAMARA")

    def guardar_ruta(self):
        global Directorio
        dialog = QFileDialog()
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        dialog.setWindowTitle("title")
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QFileDialog.Accepted:
            Directorio = dialog.selectedFiles()[0]

    def tomarfoto(self):
        global Directorio, cont, nombre, cap, text
        leido, frame = cap.read()
        if leido:
            if nombre == " ":
                nombre = "objetonoreconocido"
            dire = Directorio + "\FotoGuardada"
            if not os.path.exists(dire):
                os.makedirs(dire)
            dire = dire + "\\" + nombre + str(cont) + ".jpg"
            if not cv2.imwrite(dire, frame):
                raise Exception("No se puede guardar la imagen en: "+dire)
            text = text + "Foto tomada correctamente y guardada en: " + dire
            self.textBrowser.setText(text)
            text = text + "\n"
            cont += 1
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = ventanaui()
    GUI.show()
    sys.exit(app.exec_())
