import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

objetoClassif1 = cv2.CascadeClassifier('Martillo.xml')


def nothing(x):
    pass

cv2.namedWindow("frame")
cv2.createTrackbar("Scale", "frame", 400, 1000,nothing)
cv2.createTrackbar("Neig", "frame", 8, 20,nothing)
cv2.createTrackbar("Min Area", "frame", 0, 100000,nothing)
cv2.createTrackbar("Brightness", "frame", 180, 255, nothing)


while True:

        camBrightness = (cv2.getTrackbarPos("Brightness","frame"))
        cap.set(10,camBrightness)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        scaleVal = 1 + (cv2.getTrackbarPos("Scale","frame"))
        neig = cv2.getTrackbarPos("Neig","frame")

        objeto1 = objetoClassif1.detectMultiScale(gray,scaleVal,neig)

        for (x,y,w,h) in objeto1:
            area = w*h
            minArea = cv2.getTrackbarPos("Min Area","frame")
            if area>minArea:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.putText(frame,'Martillo',(x,y-10),2,0.7,(0,255,0),2,cv2.LINE_AA)

        cv2.imshow('frame',frame)

        if cv2.waitKey(1) == 27: break

cap.release()
cv2.destroyAllWindows()