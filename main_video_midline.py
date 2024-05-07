import cv2 as cv
import numpy as np

from image_read import image_read
from colour_filter import colour_filter
from get_contours import get_contours
from contour_filters import contour_filter_4

from midline_coords import midline_coords
from pinehsv_to_cvhsv import pinehsv_to_cvhsv

# Colours are in HSV
# Range is 0-180, 0-255, 0-255

yellow_min = (20, 100, 100)
yellow_max = (30, 255, 255)

# Colour for dilon webcam

pine_blue_min = (190, 30, 70)
pine_blue_max = (205, 100, 100)

# # Colour for mac cam

# pine_blue_min = (210, 30, 50)
# pine_blue_max = (220, 100, 100)

blue_min = pinehsv_to_cvhsv(pine_blue_min)
blue_max = pinehsv_to_cvhsv(pine_blue_max)

capture = cv.VideoCapture(1)
capture.set(3, 128)
capture.set(4, 96)

while True:

    retval, frame = capture.read() 

    if not retval:
        break
    
    blank_frame = np.zeros_like(frame)

    frame_resize = frame
    frame_blur = frame_resize
    frame_blue = colour_filter(frame_blur, blue_min, blue_max, 5, 5, 0)
    frame_yellow = colour_filter(frame_blur, yellow_min, yellow_max, 5, 5, 0)

    # Colour is in BGR

    blue_coords = midline_coords(frame_blue)
    if len(blue_coords) == 0:
        True
    else:
        for point1, point2 in zip(blue_coords, blue_coords[1:]): 
            cv.line(frame, point1, point2, [0, 255, 255], 2) 

    yellow_coords = midline_coords(frame_yellow)
    if len(yellow_coords) == 0:
        True
    else:
        for point1, point2 in zip(yellow_coords, yellow_coords[1:]): 
            cv.line(frame, point1, point2, [255, 0, 0], 2) 
    
    cv.imshow('frame', frame)
    key = cv.waitKey(1)

    if key == ord('f'):
        break

    elif key == ord('p'):
        cv.waitKey(-1)

    # elif key == ord('r'):
    #     capture = cv.VideoCapture(video)