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

def detect_face(img, classifier):
    print('DETECT_FACE')
    # create two tone img copy 
    # detect on grey, work with colored
    grey_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # get the face
    faces = classifier.detectMultiScale(grey_frame, 1.3, 5)
    # check how many faces
    if len(faces) > 1:
        # set largest
        target = (0,0,0,0)
        for i in faces:
            if i[3] > target[3]:
                target = i
        target = np.array([i], np.int32)
    elif len(faces) == 1:
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
        # ignore the bottom half if 'eye' detected
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

def blob(img, detector, threshold):
    print('BLOB')
    grey_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    # reduce image 'noise'
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=4)
    img = cv2.medianBlur(img, 5)
    coords = detector.detect(img)
    print(coords)
    return coords

# Open CV track bar requires a function call when 
# the bar when the value is changed 
def track_bar_req(val):
    print('TRACK_BAR_REQ')
    pass

print('BEFORE: MAIN')
# Using the web cam feed to input into the eye detection functions 
def main():
    # vc: video capture
    vc_img = cv2.VideoCapture(0)
    cv2.namedWindow('processed_image')
    cv2.createTrackbar('threshold', 'processed_image', 0, 255, track_bar_req)
    print('MAIN: BEFORE WHILE BLOCK')
    while True:
        print('MAIN: WHILE BLOCK')
        _, frame = vc_img.read()
        vc_frame = detect_face(frame, face_cascade)
        if vc_frame is not None:
            eyes = detect_eyes(vc_frame, eye_cascade)
            for eye in eyes:
                if eye is not None:
                    threshold = cv2.getTrackbarPos('threshold', 'processed_image')
                    eye_frame = ignore_brow(eye)
                    keypoints = blob(eye_frame, detector)
                    eye = cv2.drawKeypoints(eye_frame, keypoints, eye_frame (0,255,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        cv2.imshow('processed_image', vc_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vc_img.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()




