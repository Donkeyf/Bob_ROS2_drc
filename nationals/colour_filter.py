import cv2 as cv
import numpy as np

def colour_filter(frame, colour_min, colour_max, kernel_size=25, open=3, close=3):

    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # frame_h, frame_s, frame_v = cv.split(frame_hsv)

    kernel = np.ones((kernel_size,kernel_size),np.uint8)

    frame_colour = cv.inRange(frame_hsv, colour_min, colour_max)
    for i in range(open):
        frame_colour = cv.morphologyEx(frame_colour, cv.MORPH_OPEN, kernel)
    for i in range(close):
        frame_colour = cv.morphologyEx(frame_colour, cv.MORPH_CLOSE, kernel)

    return frame_colour