import cv2
import dlib
import numpy as np

def save_to_file(lx, ly, rx, ry):
    # save
    writeToFile.write(str(lx) + " " + str(ly) + " " + str(rx) + " " + str(ry) + "\n")

def shape_to_np(shape, dtype="int"): 
	# initialize the list of (x, y)-coordinates
	coords = np.zeros((68, 2), dtype=dtype)
	# loop over the 68 facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, 68):
		coords[i] = (shape.part(i).x, shape.part(i).y)
	# return the list of (x, y)-coordinates
	return coords

def eye_on_mask(mask, side):
    points = [shape[i] for i in side]
    points = np.array(points, dtype=np.int32)
    mask = cv2.fillConvexPoly(mask, points, 255)
    return mask

def contouring(thresh, mid, img, right=False):
    _ , cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    try:
        cnt = max(cnts, key = cv2.contourArea)
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print('MID VALUE: ' ,mid)
        if right:
            cx += mid
            # Save right x,y
            global right_x 
            right_x = cx
            global right_y
            right_y = cy
            #print("Right x,y: ", cx, cy)
            #print('RIGHT MID VALUE: ' ,mid)
        else:
            # save left x,y
            global left_x
            left_x = cx
            global left_y
            left_y = cy
            #print("Left x,y: ", cx, cy)
            #print('LEFT MID VALUE: ' ,mid)
        # draw circle on eyes
        cv2.circle(img, (cx, cy), 4, (0, 0, 255), 2)
        #print('')
    except:
        pass

def nothing(x):
    pass

# initialise left and right x,y
left_x = 0
left_y = 0
right_x = 0
right_y = 0

# open file to save eye coordinates
writeToFile = open("eye-coordinates.txt", "w")

# When record is True, x,y coords are saved to file
record = False
prompt1 = '' #"Press 'R' to Start Recording Data: "
prompt2 = '' #"Press 'ESC' to Exit: "

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_68.dat')

left = [36, 37, 38, 39, 40, 41]
right = [42, 43, 44, 45, 46, 47]

cap = cv2.VideoCapture(0)
ret, img = cap.read()
thresh = img.copy()

cv2.namedWindow('image')
kernel = np.ones((9, 9), np.uint8)

# initialise threshold slider
cv2.createTrackbar('threshold', 'image', 0, 255, nothing)

## Red Dot
# height and width of web cam frame
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
offset = 25
# Red Dot center point
dot_cx = round(width / 2)
dot_cy = round(height / 2)
# direction
dx = 1
dy = 0
# speed
speed = 10

# start dot in center of screen
x = dot_cx
y = dot_cy
counter = 0

while(True):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    for rect in rects:

        shape = predictor(gray, rect)
        shape = shape_to_np(shape)
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        mask = eye_on_mask(mask, left)
        mask = eye_on_mask(mask, right)
        mask = cv2.dilate(mask, kernel, 5)
        eyes = cv2.bitwise_and(img, img, mask=mask)
        mask = (eyes == [0, 0, 0]).all(axis=2)
        eyes[mask] = [255, 255, 255]
        mid = (shape[42][0] + shape[39][0]) // 2
        eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)
        threshold = cv2.getTrackbarPos('threshold', 'image')
        _, thresh = cv2.threshold(eyes_gray, threshold, 255, cv2.THRESH_BINARY)
        thresh = cv2.erode(thresh, None, iterations=2) #1
        thresh = cv2.dilate(thresh, None, iterations=4) #2
        thresh = cv2.medianBlur(thresh, 3) #3
        thresh = cv2.bitwise_not(thresh)
        contouring(thresh[:, 0:mid], mid, img)
        contouring(thresh[:, mid:], mid, img, True)

        # only save when 'R' is pressed, to avoid picking up 0,0,0,0
        if(record == False):
            cv2.putText(img, prompt1, (90, 195), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
        else:
            cv2.putText(img, prompt2, (90, 195), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
            # save stuff
            save_to_file(left_x, left_y, right_x, right_y)


        # call method
        #save_to_file(left_x, left_y, right_x, right_y)

        #for (x, y) in shape[36:48]:
        #   cv2.circle(img, (x, y), 2, (255, 0, 0), -1)

        # show the image with the face detections + facial landmarks
        cv2.imshow('eyes', img)

        # draw red dot in center of blue dot
        cv2.circle(img, (x, y), 10, (0, 0, 255), -1)

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
            if(x == dot_cx and y == dot_cy):
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

    #cv2.imshow("image", thresh)
    k = cv2.waitKey(1)

    # press R to record, ESC to exit
    if k == 114:
        record = True
    elif k == 27 or counter == 4:
        break

# close file and webcam
writeToFile.close()   
cap.release()
cv2.destroyAllWindows()
