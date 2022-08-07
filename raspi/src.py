import cv2 as cv
from cv2 import imshow
import numpy as np
import time
import speech_recognition as sr
import RPi.GPIO as GPIO

#load Yolo algorithm
net = cv.dnn.readNet("/home/jenishp/Projects/Python/hackathon-2022/raspi/yolov3-tiny.weights", "/home/jenishp/Projects/Python/hackathon-2022/raspi/cfg/yolov3-tiny.cfg") 
classes = []
with open("/home/jenishp/Projects/Python/hackathon-2022/raspi/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3)) #custom colors based on the object

#finding the name of object we want to detect
object_name = "apple"

""" #detect speech 
recognizer = sr.Recognizer()
index = 13
mic = sr.Microphone(device_index = index, chunk_size=1024, sample_rate=48000)

while (True):
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Say something!")
            #record audio for 5 seconds
            audio = recognizer.listen(source, phrase_time_limit = 5)

            transcript = recognizer.recognize_google(audio)
            transcript = transcript.lower()

            print(f"You said: {transcript}")
            try:
                object_name = list(set(classes) & set(transcript.split(" ")))[0] #using intersection of sets to know the desired object
                break
            except:
                print("Object out of range. Please try again.\n")
                object_name = ""
                continue
    except Exception:
        recognizer = sr.Recognizer()
        continue """



#Loading video
# cap = cv.VideoCapture('https://192.168.0.115:8080/video') #ipwebcam 
cap = cv.VideoCapture(0) #webcam 

font = cv.FONT_HERSHEY_SIMPLEX
starting_time = time.time() 
frame_id = 0 

while True and object_name != "": #change this condition once we have the hardware
    _, frame = cap.read()
    #frame = cv.resize(frame, None, fx=0.4, fy=0.4) #use if needed to resize
    frame_id += 1

    height, width, channels = frame.shape

    # Detecting objects
    blob = cv.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False) #320, 320 for faster detection, 416, 416 for better detection

    net.setInput(blob)
    outs = net.forward(output_layers)


    #showing information on the screen
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5: # 0.5 is the confidence threshold
                # Object has been detected

                # Center coords and width and height of object
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)

                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Perform non maximum suppression
    indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4) #removes multiple detections of the same object/ creates a list of the best detections of that object
    
    #draw a box around the desired object
    for i in range(len(boxes)):
        if i in indexes and classes[class_ids[i]] == object_name:
            x, y, w, h = boxes[i]
            color = colors[class_ids[i]]
            label = str(classes[class_ids[i]])

            #display the confidence
            print("Confidence: "+str(confidences[i]*100)+"% ")
            print("Center coords: (" + str(x + w/2) + ", " + str(y + h/2) + ") ")
            print("Width: " + str(w) + ", Height: " + str(h))

            #to find depth of object
            area = w*h
            k = 562250
            depth = k/area
            print("Depth : " + str(depth) + " cm\n")
        #else: 
        #    print(object_name + " not detected.\n")
   
    if(depth < 10):
        led = 18
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.HIGH)
    GPIO.cleanup()


    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    #print("FPS: " + str(fps) + "\n") 


cap.release()
cv.destroyAllWindows()