import cv2
import numpy as matrix

paint_width = 640
paint_height = 480
# function defined to be able to access the webcam
paint_frame = cv2.VideoCapture(0)
# 3-id for width
paint_frame.set(3, paint_width)
# 4-id for height
paint_frame.set(4, paint_height)
# 10-id for brightness
paint_frame.set(10, 150)

# valorile culorilor care vor fi detectate: -HSV
colors = [[48, 90, 171, 179, 111, 255],  # roz
            [0, 116, 155, 12, 172, 255],  # portocaliu
            [75, 86, 103, 92, 159, 249]  # verde
           ]

#  Format culori BGR- aceste se vor afisa pe ecran
# roz        230, 9, 204
# portocaliu 245, 164, 66
# verde      92, 173, 95

# for each identified color we define the color we want to draw with
color_draw = [[204, 9, 203],
              [66, 164, 245],  ##BGR
              [95, 173, 95]
             ]

points = []  # [x,y,colorID]


def find_color(img, color, color_draw):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # counter to be able to access from the color_draw the color that corresponds to the colors
    i = 0
    # vector for points we want to draw
    new_points = []
    for current_color in color:
        #minim values for hue,saturation and value
        lower = matrix.array(current_color[0:3])
        #maxim values for hue, saturation and value
        upper = matrix.array(current_color[3:6])
        #create masc
        mask = cv2.inRange(img_hsv, lower, upper)
        #get the coordinates of the point we want to draw
        x, y = getContours(mask)
        #cv2.circle(img_result, (x, y), 10, color_draw[i], cv2.FILLED)
        #check that the coordinates of point are different from 0, if so add the point
        if x != 0 and y != 0:
            new_points.append([x, y, i])
        i += 1
    return new_points


def getContours(img):
    # retrieves the extreme outer contours
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    # go through the contour vector
    for cnt in contours:
        # calculate area
        area = cv2.contourArea(cnt)
        print(area)
        #eliminate the unwanted surfaces
        if area > 500:
            # cv2.drawContours( img_result, cnt, -1, (255, 0, 0), 3)
            #calculate perimter for contour
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            #retrieve coordinates for first point in the rectangle, weight, height
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def draw_on_canvas(points, color_draw):
    for point in points:
        cv2.circle(img_result, (point[0], point[1]), 10, color_draw[point[2]], cv2.FILLED)


while True:
    #read imagine
    success, img = paint_frame.read()
    #create imagine that will show after we draw
    img_result = img.copy()
    new_points = find_color(img, colors, color_draw)
    #display the points
    if len(new_points) != 0:
        for newP in new_points:
            points.append(newP)
    if len(points) != 0:
        draw_on_canvas(points, color_draw)
    cv2.imshow("Result", img_result)
    if cv2.waitKey(1) & 0xFF == ord('a'):
        break