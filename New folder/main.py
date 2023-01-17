import mediapipe as mp
import cv2
from pyfirmata import Arduino,SERVO,util
from time import sleep
#import requests

#URL = "http://192.168.1.34"

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
smile_cascade=cv2.CascadeClassifier("smile.xml")
port = "COM6"
pin = 10
#pin2 = 11
board = Arduino(port)
board.digital[pin].mode = SERVO
#board.digital[pin2].mode = SERVO
ledL = board.get_pin('d:9:o')
ledR = board.get_pin('d:11:o')


def on(ledPin):
    ledPin.write(1)
def off(ledPin):
    ledPin.write(0)

cap = cv2.VideoCapture(0)
#address = "https://192.168.8.102:8080/video"
#cap.open(address)

video = cv2.VideoWriter('webcam.avi', cv2.VideoWriter_fourcc(*'MP42'), 20.0, (640, 480))
record = False

tracker = cv2.legacy.TrackerMOSSE_create() #------------
ret, frame = cap.read() #------------
image = cv2.flip(frame, 1)
#image = cv2.rotate(image, cv2.ROTATE_180)
bbox = cv2.selectROI("Personal Robot Photographer",image,False) #------------
tracker.init(image,bbox) #------------


def map_rangeX(x):
    return (x - 0) * (256 - 0) // (635 - 0) + 0

#def map_rangeY(y):
    #return (y - 0) * (180 - 0) // (480 - 0) + 0

def drawBox(img,bbox): #------------
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]) #------------
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,255,0),3,1) #------------
    print(map_rangeX(x))
    if map_rangeX(x) <= 0:
        rotateServo(pin, 0)
        on(ledR)
        off(ledL)
    #elif map_rangeX(x) <=50 and map_rangeX(x) <=100:
        #rotateServo(pin, 90)
        #on(ledR)
        #on(ledL)
    else:
        #requests.get(url=URL,params={'led': str(map_rangeX(x))})
        rotateServo(pin, map_rangeX(x))
        on(ledL)
        on(ledR)
        #rotateServo(pin, 90)
    if map_rangeX(x) >= 175:
        on(ledL)
        off(ledR)

def rotateServo(pin,angle):
    board.digital[pin].write(angle)
    sleep(0.015)

#rotateServo(pin,90)
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read() #------------
        # Flip on horizontal
        image = cv2.flip(frame, 1)
        #image = cv2.rotate(image, cv2.ROTATE_180)
        #image = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE)
        ret, bbox = tracker.update(image) #------------
        drawBox(image, bbox) #------------
        # BGR 2 RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Set flag
        image.flags.writeable = False
        # Detections
        results = hands.process(image)
        # Set flag to true
        image.flags.writeable = True
        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if record == False:
            # Rendering results
            if results.multi_hand_landmarks:
                for num, hand in enumerate(results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                              mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2,
                                                                     circle_radius=2),
                                              )
                if results.multi_handedness[0].classification[0].label == 'Left':
                    record = True
                    video.write(frame)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            #for x, y, w, h in face:
                #image=cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),3)
                #smile = smile_cascade.detectMultiScale(gray, scaleFactor=1.8, minNeighbors=20)
                # print(type(x))
                #print("Not mapped: ")
                #print(x.item())
                #firebase.put('/centerX/', 'a', x.item())
                #print(map_rangeX(x.item()))
                #rotateServo(pin,map_rangeX(x.item()))
                #rotateServo(pin2, map_rangeY(y.item()))
            smile = smile_cascade.detectMultiScale(gray, scaleFactor=1.8, minNeighbors=20) #------------
            for x, y, w, h in smile:
                image=cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),3)
                cv2.imwrite('c1.png', frame)
                    #notification.audio = "shutter.wav"
                    #notification.send()

            cv2.imshow('Personal Robot Photographer', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        else:
            video.write(frame)
            # Rendering results
            if results.multi_hand_landmarks:
                for num, hand in enumerate(results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                              mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2,
                                                                     circle_radius=2),
                                              )
                if results.multi_handedness[0].classification[0].label == 'Right':
                    video.release()
                    record = False
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            #for x, y, w, h in face:
                #image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3)
                #smile = smile_cascade.detectMultiScale(gray, scaleFactor=1.8, minNeighbors=20)
                # print(type(x))
                #print("Not mapped: ")
                #print(x.item())
                # firebase.put('/centerX/', 'a', x.item())
                #print(map_rangeX(x.item()))
                #rotateServo(pin, map_rangeX(x.item()))
                # rotateServo(pin2, map_rangeY(y.item()))
            smile = smile_cascade.detectMultiScale(gray, scaleFactor=1.8, minNeighbors=20) #------------
            for x, y, w, h in smile:
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 3)
                cv2.imwrite('c1.png', frame)
                    # notification.audio = "shutter.wav"
                    # notification.send()

            cv2.imshow('Personal Robot Photographer', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()