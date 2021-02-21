

import cv2
import dlib
import numpy as np

# set face data - https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# set eye data - https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# import image for testing
img = cv2.imread('trump.jpg')

# create grey scale
grey_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# start with bigger target, the face
# faces: an array of arrays - [[x,y,w,h], [x,y,w,h], [x,y,w,h], [x,y,w,h]]
faces = face_cascade.detectMultiScale(grey_scale, 1.3, 5)
# draw box around face
# start at fx,fy
# of size fw,fh
for (fx, fy, fw, fh) in faces:
    cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), (255,255,0), 2) # color and thickness

# now pick out the eyes from face frame
# cut out grey face frame
grey_face = grey_scale[fy:fy+fh, fx:fx+fw]
# cut out detected face frame
detected_face = img[fy:fy+fh, fx:fx+fw]
# eyes: an array of arrays
eyes = eye_cascade.detectMultiScale(grey_face)

# draw box around eyes
# start at ex,ey
# of size ew,eh
for (ex, ey, ew, eh) in eyes:
    cv2.rectangle(detected_face, (ex, ey), (ex + ew, ey + eh), (255,255,0), 2) # color and thickness

# default.jpg - program detects chin as eye
# face.jpg - program detects left nostral as eye
# to prevent the detection of anything other than the eyes 
# we will ignore the bottom half of the image
def detect_eyes(img, classifier):
    # create two tone img copy 
    grey_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(grey_frame, 1.3, 5)
    coords = cascade.detectMultiScale(img_grey, 1.3, 5)
    height = np.size(image, 0)
    for (x,y,w,h) in coords
        # ignore the bottom half if eye 'detected'
        if y+h > height/2:
            pass



# show results of face detection
cv2.imshow('face detected', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


