import cv2
import os
import imutils
import numpy as np

captura = cv2.VideoCapture(0,cv2.CAP_DSHOW)


while True:

    ret, frame = captura.read()
    if ret == False : break

    # cambiar imagen de color a gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # volver la imagen gris a una binaria
    _, th = cv2.threshold(gray, 140, 240,
    cv2.THRESH_BINARY)  # los numeros cambian (menor el numero es mas blanco, mayor el numero mas oscuro)

    # encontrar los contornos de la imagen binaria (solo encuentra en imagenes binarias)
    contornos, hierarchy = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # muestra 3 ventas, la imagen binaria, la imagen capturada y la imagen con contornos
    cv2.imshow('Binaria', th)
    cv2.imshow('Video', frame)
    # dentro del imshow se llama a los contornos dibujados, no hacer fuera porque no imprimiria el video sin contornos
    cv2.imshow('Contornos', cv2.drawContours(frame, contornos, -1, (0, 255, 0), 2))

    total = 0
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 1700:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                cv2.imshow('rectangulo', cv2.drawContours(frame, [approx], -1, (255, 0, 0), 2, cv2.LINE_AA))
                total += 1

    mesa = 'Mesa: ' + str(total)
    cv2.imshow('Mesas: ', cv2.putText(frame, mesa, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


captura.release()
cv2.destroyAllWindows()
