import cv2 as cv
from cv2 import imshow
import numpy as np
import time
import speech_recognition as sr

#load Yolo algorithm
net = cv.dnn.readNet("sTobjDetection/yolov3-tiny.weights", "sTobjDetection/cfg/yolov3-tiny.cfg") #load yolov3-tiny.weights and yolov3-tiny.cfg if fps is too low
classes = []
with open("sTobjDetection/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
#print(classes)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3)) #custom colors based on the object

#finding the name of object we want to detect
# object_name = "apple"

#detect speech 
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
        continue


# Loading image
""" img = cv.imread("testingData/img/cat.jpg")
img = cv.resize(img, None, fx=0.4, fy=0.4)
"""

#Loading video
#cap = cv.VideoCapture("data/videos/cat.mp4") #cat.mp4
cap = cv.VideoCapture(0) #webcam 
#cap = cv.VideoCapture('https://192.168.0.115:8080/video') #webcam 

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

    """ #print the blob for each rgb channels
    for b in blob:
        for n, img_blob in enumerate(b):
            imshow(str(n), img_blob) """

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
            cv.rectangle(frame, (x, y), (x + w, y + h), color, thickness = 2)
            cv.putText(frame, label, (x, y - 5), font, 1, color, thickness = 2)

            #display the confidence
            cv.putText(frame, str(round(confidences[i]*100,2))+"%", (x+w-100, y - 5), font, 1, color, thickness = 2)
            print("Center coords: (" + str(x + w/2) + ", " + str(y + h/2) + ")")
            print("Width: " + str(w) + ", Height: " + str(h))

            """ #to find depth of object
            area = w*h
            k = 562250
            depth = k/area
            print(", Depth : " + str(depth) + " cm\n") """
        else: 
            print(object_name + " not detected.\n")
   
    
    """ #draw box around all objects
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv.rectangle(frame, (x, y), (x + w, y + h), color, thickness = 2)
            cv.putText(frame, label, (x, y - 5), font, 1, color, thickness = 2)
            #display the confidence
            cv.putText(frame, str(round(confidences[i]*100,2))+"%", (x+w-100, y - 5), font, 1, color, thickness = 2) """
   

    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    cv.putText(frame, "FPS: " + str(round(fps, 2)), (5, 30), font, 1, (0, 255, 0), thickness = 2) 

    #print the video frame we've worked with
    imshow('Real time object detection', frame)
    key = cv.waitKey(1)
    if key == 27:
        break

cap.release()
cv.destroyAllWindows()

#best quality detection configuration: yolov3.weights and yolov3.cfg with 416x416 resolution
#best speed configuration: yolov3-tiny.weights and yolov3-tiny.cfg with 320x320 resolution

#compromise: yolov3-tiny.weights and yolov3-tiny.cfg with 416x416 resolution