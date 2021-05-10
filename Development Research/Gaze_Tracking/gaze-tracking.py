import cv2

# Gaze Tracking is a Python library that provides a webcam-based eye tracking system. It gives us the exact position of the pupils and the gaze direction, in real time.
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Opens a file in which we write the left and right eye coordinates too.
# writeToFile = open("eye-coordinates.txt", "w")
writeToFileFormat = open("eye-coordinatesFormat.txt", "w")
record = False
prompt1 = "Press 'R' to Start Recording Data: "
prompt2 = "Press 'ESC' to Exit: "

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

    # === Test Code ===
    if(record == False):
        cv2.putText(frame, prompt1, (90, 195), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)

    else:
        # need to format fot use in numpy
        cv2.putText(frame, prompt2, (90, 195), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
        if(left_pupil != None or right_pupil != None):
            left_eye_x = left_pupil[0]
            left_eye_y = left_pupil[1]
            right_eye_x = right_pupil[0]
            right_eye_y = right_pupil[1]
            print(left_eye_x, left_eye_y, right_eye_x, right_eye_y)
            writeToFileFormat.write(str(left_eye_x) + " " + (str(left_eye_y))  + " " + (str(right_eye_x)) + " " + (str(right_eye_y)) + "\n") 

    # ==================

    # write the left and right eye coordinates to the file.
    # writeToFile.write(str(left_pupil) + " " + str(right_pupil) + "\n")

    # putText() is used to draw the text string onto the screen.
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    # imshow() is used to display a image in a window.
    cv2.imshow("Demo", frame)

    k = cv2.waitKey(1)

    # press R to record, ESC to exit
    if k == 114:
        record = True
    elif k == 27:
        break