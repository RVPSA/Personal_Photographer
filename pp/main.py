import cv2
from firebase import firebase
from notifypy import Notify

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
smile_cascade=cv2.CascadeClassifier("smile.xml")
firebase = firebase.FirebaseApplication('https://personalrobotcoordinate-default-rtdb.firebaseio.com', None)
cor = 90
firebase.put('/centerX:','a',cor)
notification = Notify()

video=cv2.VideoCapture(0)
#video=cv2.VideoCapture(1) when using usb cam
#address = "https://192.168.43.203:8080/video" when using ip web cam
#video.open(address)

while True:
    check,frame=video.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    face=face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)
    for x,y,w,h in face:
        #img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
        smile=smile_cascade.detectMultiScale(gray,scaleFactor=1.8,minNeighbors=20)
        #print(type(x))
        print(x.item())
        firebase.put('/centerX/', 'a', x.item())
        for x,y,w,h in smile:
            #img=cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
            #cv2.imwrite('c1.png', frame)
            notification.audio = "shutter.wav"
            notification.send()

    cv2.imshow('gotcha',frame)
    #print(type(cor))
    #firebase.put('/centerX:', 'a', cor)
    key=cv2.waitKey(1)

    if key==ord('q'):
         break

video.release()
cv2.destroyAllWindows
