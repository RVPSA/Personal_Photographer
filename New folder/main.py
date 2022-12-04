import mediapipe as mp
import cv2
#from firebase import firebase
#import numpy as np
#import uuid
#import os
from pyfirmata import Arduino,SERVO,util
from time import sleep

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
smile_cascade=cv2.CascadeClassifier("smile.xml")
#firebase = firebase.FirebaseApplication('https://personalrobotcoordinate-default-rtdb.firebaseio.com', None)
port = "COM3"
pin = 10
#pin2 = 11
board = Arduino(port)
board.digital[pin].mode = SERVO
#board.digital[pin2].mode = SERVO

cap = cv2.VideoCapture(0)
video = cv2.VideoWriter('webcam.avi', cv2.VideoWriter_fourcc(*'MP42'), 20.0, (640, 480))
record = False

def map_rangeX(x):
    return (x - 0) * (180 - 0) // (640 - 0) + 0

#def map_rangeY(y):
    #return (y - 0) * (180 - 0) // (480 - 0) + 0

def rotateServo(pin,angle):
    board.digital[pin].write(angle)
    sleep(0.015)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        if record == False:
            ret, frame = cap.read()
            # BGR 2 RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Flip on horizontal
            image = cv2.flip(image, 1)
            # Set flag
            image.flags.writeable = False
            # Detections
            results = hands.process(image)
            # Set flag to true
            image.flags.writeable = True
            # RGB 2 BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
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
            face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for x, y, w, h in face:
                image=cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),3)
                smile = smile_cascade.detectMultiScale(gray, scaleFactor=1.8, minNeighbors=20)
                # print(type(x))
                print("Not mapped: ")
                print(x.item())
                #firebase.put('/centerX/', 'a', x.item())
                print(map_rangeX(x.item()))
                rotateServo(pin,map_rangeX(x.item()))
                #rotateServo(pin2, map_rangeY(y.item()))

                for x, y, w, h in smile:
                    image=cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),3)
                    #cv2.imwrite('c1.png', frame)
                    #notification.audio = "shutter.wav"
                    #notification.send()

            cv2.imshow('Personal Robot Photographer', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        else:
            ret, frame = cap.read()
            # BGR 2 RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Flip on horizontal
            image = cv2.flip(image, 1)
            # Set flag
            image.flags.writeable = False
            # Detections
            results = hands.process(image)
            # Set flag to true
            image.flags.writeable = True
            # RGB 2 BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
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
            face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for x, y, w, h in face:
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3)
                smile = smile_cascade.detectMultiScale(gray, scaleFactor=1.8, minNeighbors=20)
                # print(type(x))
                print("Not mapped: ")
                print(x.item())
                # firebase.put('/centerX/', 'a', x.item())
                print(map_rangeX(x.item()))
                rotateServo(pin, map_rangeX(x.item()))
                # rotateServo(pin2, map_rangeY(y.item()))
                for x, y, w, h in smile:
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 3)
                    #cv2.imwrite('c1.png', frame)
                    # notification.audio = "shutter.wav"
                    # notification.send()

            cv2.imshow('Personal Robot Photographer', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()