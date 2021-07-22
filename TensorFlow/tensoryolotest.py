import cv2
import numpy as np
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon, QPixmap

cap = cv2.VideoCapture(0)
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
    for i in indices:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%',
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)


class ventanaui(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.btn0.clicked.connect(self.activar)
        self.btn0.clicked.connect(self.viewCam)
        self.btn1.clicked.connect(self.desactivar)

    def activar(self):
        self.btn0.setEnabled(False)
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(True)
        self.btn3.setEnabled(True)

    def desactivar(self):
        global cap
        cap.release()
        self.btn0.setEnabled(True)
        self.btn1.setEnabled(False)
        self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)
        self.lblVideo.setPixmap(QPixmap('x2.jpg'))

    def viewCam(self):
        global cap
        while cap.isOpened():
            success, img = cap.read()
            blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
            net.setInput(blob)
            layerNames = net.getLayerNames()
            outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
            outputs = net.forward(outputNames)
            findObjects(outputs, img)
            if success == True:
                self.displayImage(img)
                cv2.waitKey(1)
            else:
                self.activar()
                self.errorcamara()

    def displayImage(self, img, window=1):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = ventanaui()
    GUI.show()
    sys.exit(app.exec_())
