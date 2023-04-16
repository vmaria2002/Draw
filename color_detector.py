import cv2
import numpy as matrix


def empty(a):
    pass


frame_width = 350
frame_height = 480
# function defined to be able to access the webcam
frame = cv2.VideoCapture(0)
# 3-id for width 350
frame.set(3, frame_width)
# 4-id for height
frame.set(4, frame_height)
# create the window in which we will display the properties of the hue image, saturation and value
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
# create a trackbar for hue, saturation, and value
# that will help us define these values for each color we want to identify
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

while True:
    success, img = frame.read()
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # get the minum and maximum values from trackbar
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    print(h_min)
    # store  minimum and maximum values in vectors
    lower = matrix.array([h_min, s_min, v_min])
    upper = matrix.array([h_max, s_max, v_max])
    # a binary mask is returned, where white pixels(255) represent pixels
    # that fall into the upper and lower limit range and black pixels(0) do not.
    mask = cv2.inRange(img_hsv, lower, upper)
    # apply the mask on the original image so we can see the color
    result = cv2.bitwise_and(img, img, mask=mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    # combine the 3 images into one
    h_stack = matrix.hstack([img, mask, result])
    cv2.imshow('Horizontal Stacking', h_stack)
    # the stopping condition that  will close our window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Closes video file or capturing device.
frame.release()
# simply  destroys all the windows we created.
cv2.destroyAllWindows()