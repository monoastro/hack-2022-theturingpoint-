
import cv2
import numpy as np
import pyttsx3
import os
import pyaudio
from simple_facerec import SimpleFacerec


sfr = SimpleFacerec()
sfr.load_encoding_images("faceDetection/images/")
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()

    #detrcface
    face_location, face_name=  sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_location, face_name):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        
        cv2.putText(frame, name, (x1, y1- 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,200),2)
        cv2.rectangle(frame,(x1,y1),(x2, y2), (0,0,200),2)
        if name != "Unknown":
            engine= pyttsx3.init()
            rate = engine.getProperty("rate")

            engine.setProperty("rate", 80)
            engine.say("Hello "+ name )
            engine.runAndWait()
    cv2.imshow("Satish Detection Algorithm",frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows(0)

