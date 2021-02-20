import cv2
import dlib
import numpy as np

# set face data - https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# set eye data - https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye')

# import image for testing
img = cv2.imread('trump.jpg')

# create grey scale
grey_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# start with bigger target, the face
# face: an array of arrays - [[x,y,w,h], [x,y,w,h], [x,y,w,h], [x,y,w,h]]
face = face_cascade.detectMultiScale(grey_scale, 1.3, 5)
# draw box around face
# start at x,y
# of size w,h
for (fx, fy, fw, fh) in face:
    cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), (255,255,0), 2) # color and thickness

# now pick out the eyes from face frame


# draw box around eyes


# show results of face detection
cv2.imshow('face detected', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Read image in
#img = cv2.imread('image.png')
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale detector = dlib.get_frontal_face_detector()
#rects = detector(gray, 1) # rects contains all the faces detected

