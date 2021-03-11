# Adapted from: https://medium.com/@stepanfilonov/tracking-your-eyes-with-python-3952e66194a6
import cv2
import dlib
import numpy as np
import logging as log

# Initialise OpenCV 
# set face and eye data
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# blob - initialize paramaters
parameters = cv2.SimpleBlobDetector_Params()
parameters.filterByArea = True
parameters.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(parameters)

# import image for testing and create grey scale of it 
img = cv2.imread('default.jpg')
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

# blob detection algo used for tracking
threshold = 42
_, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

def detect_face(img, classifier):
    print('DETECT_FACE')
    # create two tone img copy 
    # detect on grey, work with colored
    grey_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # get the face
    faces = classifier.detectMultiScale(grey_frame, 1.3, 5)
    # check how many faces
    if len(faces > 1):
        # set largest
        target = (0,0,0,0)
        for i in faces:
            if i[3] > target[3]:
                target = i
        target = np.array([i], np.int32)
    elif len(faces == 1):
        target = faces
    else:
        log.warning('detect_face(): error reading image, no face detected')
        return None
    # frame the detected face
    for(x,y,w,h) in target:
        frame = img[y:y+h, x:x+w]
    return frame

def detect_eyes(img, classifier):
    print('DETECT_EYES')
    # create two tone img copy 
    grey_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # get the eyes
    eyes = classifier.detectMultiScale(grey_frame, 1.3, 5)
    # get frame height and width  
    height = np.size(img, 0)
    width = np.size(img, 1)
    left_eye = None
    right_eye = None
    for (x, y, w, h) in eyes:
        # ignore the bottom half if eye 'detected'
        if y > height/2:
            pass
        eye_center = x + w / 2
        if eye_center < width * 0.5:
            left_eye = img[y:y+h, x:x+w]
        else:
            right_eye = img[y:y+h, x:x+w]
    return left_eye, right_eye

def ignore_brow(img):
    print('IGNORE_BROW')
    # set height and width to the images values
    height, width = img.shape[:2]
    # set eye brow line estimate
    brow_height = int(height/4)
    # cut out new image
    img = img[brow_height:height, 0:width]
    return img

def blob(img, detector):
    print('BLOB')
    grey_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    # reduce image 'noise'
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=4)
    img = cv2.medianBlur(img, 5)
    coords = detector.detect(img)
    return coords

keypoints = blob(img, detector)
cv2.drawKeypoints(img, keypoints, img, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# show results of detection
cv2.imshow('face detected', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


