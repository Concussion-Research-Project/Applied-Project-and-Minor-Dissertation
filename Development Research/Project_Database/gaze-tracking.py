import cv2
from pymongo import MongoClient
import json
import csv
import pandas as pd
import sys, getopt, pprint
from datetime import datetime

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('mongodb+srv://research-project:cGeNVHwDOQBIjXAM@cluster0.mrfjn.mongodb.net/clients?retryWrites=true&w=majority')

db=client.clients
#collection = db.test   # and inside that DB, a collection called "files"
collectionBase = db.base
collectionTest2 = db.test2

def eyeTracker():
    # Gaze Tracking is a Python library that provides a webcam-based eye tracking system. It gives us the exact position of the pupils and the gaze direction, in real time.
    from gaze_tracking import GazeTracking

    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)

    # Opens a file in which we write the left and right eye coordinates too.
    writeToFile = open("eye-coordinates.txt", "w")
    writeToFileCSV = open("eye-coordinatesCSV.csv", "w")

    record = False
    prompt1 = "Press 'R' to Start Recording Data: "
    prompt2 = "Press 'ESC' to Exit: "

    # height and width of frame
    height = webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
    offset = 25

    # variables for dot movement

    # center point
    cx = round(width / 2)
    cy = round(height / 2)
    # direction
    dx = 1
    dy = 0
    # speed
    speed = 10

    # start dot in center of screen
    x = cx
    y = cy
    counter = 0

    #print("center x :", x)
    #print("center y :", y)

    # loop webcam feed
    while True:

        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"

        # putText() is used to draw the text string onto the screen.
        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        # get the left and right eye coordinates.
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()

        # check if data is recording
        if(record == False):
            cv2.putText(frame, prompt1, (90, 195), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
        else:
            # format for use in numpy
            cv2.putText(frame, prompt2, (90, 195), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
            if(left_pupil != None and right_pupil != None):
                # ==== test code =====
                left_eye_x = (left_pupil[0] - cx)
                left_eye_y = (left_pupil[1] - cy)
                right_eye_x = (right_pupil[0] - cx)
                right_eye_y = (right_pupil[1] - cy)

                # ======= TEST CODE ======
                """
                left_eye_x = left_pupil[0]
                left_eye_y = left_pupil[1]
                right_eye_x = right_pupil[0]
                right_eye_y = right_pupil[1]
                """

                writeToFile.write(str(left_eye_x) + " " + (str(left_eye_y))  + " " + (str(right_eye_x)) + " " + (str(right_eye_y)) + "\n") 
                writeToFileCSV.write(str(left_eye_x) + ", " + (str(left_eye_y))  + ", " + (str(right_eye_x)) + ", " + (str(right_eye_y)) + "\n")
                
        # draw red dot in center of blue dot
        cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)

        # move the dot if recording
        if(record):
            # apply formula to make it move
            x += dx * speed
            y += dy * speed

            # change x-axis direction when at boundry
            if(x > (width - offset)):
                dx = -1
            elif(x < offset):
                dx = 1

            # change y-axis direction when at boundry
            if(y > (height - offset)):
                dy = -1
            elif(y < offset):
                dy = 1
        
            # change direction if at center point
            if(x == cx and y == cy):
                if(counter == 0):
                    print("counter 0 passed")
                    counter += 1
                    dx = 0
                    dy = -1
                elif(counter == 1):
                    print("counter 1 passed")
                    counter += 1
                    dx = -1
                    dy = 0
                elif(counter == 2):
                    print("counter 2 passed")
                    counter += 1
                    dx = 0
                    dy = 1
                elif(counter == 3):
                    print("counter 3 passed")
                    counter += 1
                    dx = 1
                    dy = 0

        # putText() is used to draw the text string onto the screen.
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        # imshow() is used to display a image in a window.
        cv2.imshow("Demo", frame)

        k = cv2.waitKey(1)

        # press R to record, ESC to exit
        if k == 114:
            record = True
        elif k == 27 or counter == 4:
            break

    writeToFile.close()
    writeToFileCSV.close()

    f = open('eye-coordinatesCSV.csv')  # open a file
    text = f.read()    # read the entire contents, should be UTF-8 text

    # build a document to be inserted
    # text_file_doc = {"client_id": clientFileId, "Date": todays_date, "Injury Type": injury_type, "Sport Played": sports_type, "contents" : text}

    if choice == '1':  
        # build a document to be inserted    
        text_file_doc = {"client_id": clientFileId, "Date": todays_date, "Injury Type": injury_type, "Sport Played": sports_type, "contents" : text}

        # insert the contents into the "file" collection
        collectionBase.insert(text_file_doc)
    elif choice == '2':
        # build a document to be inserted
        text_file_doc = {"client_id": clientFileId, "Date": todays_date, "Injury Type": injury_type, "Sport Played": sports_type, "contents" : text}

        # insert the contents into the "file" collection
        collectionTest2.insert(text_file_doc)

# End of eyeTracker() method

choice = input("Select one of the following: \n 1: New Patient \n 2: Existing Patient\n Choice: ")

if choice == '1':
    clientFileId = input("\n Enter client ID: ")
    todays_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    injury_type = input(" Enter injury type: ")
    sports_type = input(" Enter sport type: ")
    eyeTracker()
elif choice == '2':
    clientFileId = input("\n Enter client ID: ")
    todays_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    injury_type = input(" Enter injury type: ")
    sports_type = input(" Enter sport type: ")
    eyeTracker()