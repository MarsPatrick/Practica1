import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

objetoClassif1 = cv2.CascadeClassifier('cascade.xml')
objetoClassif2 = cv2.CascadeClassifier('cascade1.xml')
while True:

        ret,frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objeto1 = objetoClassif1.detectMultiScale(gray, scaleFactor=4, minNeighbors=91,minSize=(70,70))
        objeto2 = objetoClassif2.detectMultiScale(gray, scaleFactor=2, minNeighbors=50, minSize=(70, 78))

        for (x,y,w,h) in objeto1:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame,'Audifono',(x,y-10),2,0.7,(0,255,0),2,cv2.LINE_AA)

        for (x,y,w,h) in objeto2:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame,'Control',(x,y-10),2,0.7,(0,255,0),2,cv2.LINE_AA)
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) == 27: break

cap.release()
cv2.destroyAllWindows()