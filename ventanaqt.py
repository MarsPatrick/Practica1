from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap, QImage
import cv2
import sys


class ventanaui(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)

        self.desactivar()
        self.btn0.clicked.connect(self.activar)
        self.btn0.clicked.connect(self.viewCam)
        self.btn1.clicked.connect(self.desactivar)


    def activar(self):
        self.btn0.setEnabled(False)
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(True)
        self.btn3.setEnabled(True)

    def desactivar(self):
        self.btn0.setEnabled(True)
        self.btn1.setEnabled(False)
        self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)

    def viewCam(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap
            if ret == True:
                self.displayImage(frame,1)
                cv2.waitKey()

    def displayImage(self,img,window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape)==3:
            if(img.shape[2])==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        img=QImage(img,img.shape[1],img.shape[0],qformat)
        img=img.rgbSwapped()
        self.lblVideo.setPixmap(QPixmap.fromImage(img))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = ventanaui()
    GUI.show()
    sys.exit(app.exec_())

# XML de los objetos
objetoClassif = cv2.CascadeClassifier('cascade.xml')

def errorcamara():
    print("error")