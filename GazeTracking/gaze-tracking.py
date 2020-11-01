import cv2

# Gaze Tracking is a Python library that provides a webcam-based eye tracking system. It gives us the exact position of the pupils and the gaze direction, in real time.
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Opens a file in which we write the left and right eye coordinates too.
writeToFile = open("eye-coordinates.txt", "w")

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

    # write the left and right eye coordinates to the file.
    writeToFile.write(str(left_pupil) + " " + str(right_pupil) + "\n")

    # putText() is used to draw the text string onto the screen.
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    # imshow() is used to display a image in a window.
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
