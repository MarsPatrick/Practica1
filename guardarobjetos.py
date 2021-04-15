import cv2
import numpy as np
import imutils
import os

Datos = 'n'
if not os.path.exists(Datos):
    os.makedirs(Datos)

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

x1, y1=190, 80
x2, y2=450, 398

count=0

while True:

    ret,frame = cap.read()
    if ret == False: break
    imAux = frame.copy()
    cv2.rectangle(frame,(x1,y1),(x2,y2),(2555,0,0),2)

    objeto = imAux[y1:y2,x1:x2]
    objeto = imutils.resize(objeto,width=38)

    cv2.imshow('objeto',objeto)
    cv2.imshow('frame',frame)

    k = cv2.waitKey(1)
    if k == 27: break

    if k == ord('s'):
        cv2.imwrite(Datos+'/objeto_{}.jpg'.format(count),objeto)
        count = count + 1

cap.release()
cv2.destroyAllWindows()