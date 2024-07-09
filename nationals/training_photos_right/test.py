import cv2 as cv
import numpy as np

from image_read import image_read
from colour_filter import colour_filter
from get_contours import get_contours
from contour_filters import contour_filter_4
from pinehsv_to_cvhsv import pinehsv_to_cvhsv
from obstacle import ObstacleDetection

pine_purple_min = (310, 20, 40)
pine_purple_max = (370, 50, 70)

purple_min = pinehsv_to_cvhsv(pine_purple_min)
purple_max = pinehsv_to_cvhsv(pine_purple_max)


capture = cv.VideoCapture(1)
capture.set(3, 128)
capture.set(4, 96)

obs = ObstacleDetection()

while True:

    retval, frame = capture.read() 

    if not retval:
        break

    blank_frame = np.zeros_like(frame)
    # blank_frame = cv.copyMakeBorder(blank_frame, 1, 1, 1, 1, cv.BORDER_CONSTANT)
    # blank_frame = frame


    frame_resize = frame
    frame_blur = frame_resize
    # frame_blur = cv.GaussianBlur(frame, (45,45), 1)
    # frame_yellow = colour_filter(frame_blur, yellow_min, yellow_max, 5, 5, 0)
    # frame_blue = colour_filter(frame_blur, blue_min, blue_max, 5, 5, 0)
    frame_purple = colour_filter(frame_blur, purple_min, purple_max, 5, 5, 0)


    box = obs.obstacle_box(frame_purple)
    print(box)


