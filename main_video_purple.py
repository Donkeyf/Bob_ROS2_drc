import cv2 as cv
import numpy as np

from image_read import image_read
from colour_filter import colour_filter
from get_contours import get_contours
from contour_filters import contour_filter_4
from pinehsv_to_cvhsv import pinehsv_to_cvhsv

# Colours are in HSV
# Range is 0-180, 0-255, 0-255

pine_purple_min = (310, 20, 40)
pine_purple_max = (370, 50, 70)

purple_min = pinehsv_to_cvhsv(pine_purple_min)
purple_max = pinehsv_to_cvhsv(pine_purple_max)

capture = cv.VideoCapture(1)
capture.set(3, 128)
capture.set(4, 96)

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

    # contours_yellow = get_contours(frame_yellow)
    # contours_blue = get_contours(frame_blue)
    contours_purple = get_contours(frame_purple)
    # contours_yellow, yellow_track = contour_filter_4(contours_yellow)
    # contours_blue, blue_track = contour_filter_4(contours_blue)

    # cv.drawContours(blank_frame, contours_yellow, -1, yellow_max)
    # cv.drawContours(blank_frame, contours_blue, -1, (255, 0, 0))
    # cv.drawContours(frame, contours_yellow, -1, (255,0,0))
    # cv.drawContours(frame, contours_blue, -1, yellow_max)
    cv.drawContours(frame, contours_purple, -1, (0,0,255))

    # try:
    #         # cv.line(blank_frame, 
    #         #         np.intp((yellow_track[0] - 100 * np.cos(yellow_track[2]), yellow_track[1] + 100 * np.sin(yellow_track[2]))),
    #         #         np.intp((yellow_track[0] + 100 * np.cos(yellow_track[2]), yellow_track[1] - 100 * np.sin(yellow_track[2]))),
    #         #         yellow_max, 3)
    #         # cv.line(blank_frame, 
    #         #         np.intp((blue_track[0] - 100 * np.cos(blue_track[2]), blue_track[1] + 100 * np.sin(blue_track[2]))),
    #         #         np.intp((blue_track[0] + 100 * np.cos(blue_track[2]), blue_track[1] - 100 * np.sin(blue_track[2]))),
    #         #         (255, 0, 0), 3)
            
    #         cv.line(frame, 
    #                 np.intp((yellow_track[0] - 100 * np.cos(yellow_track[2]), yellow_track[1] + 100 * np.sin(yellow_track[2]))),
    #                 np.intp((yellow_track[0] + 100 * np.cos(yellow_track[2]), yellow_track[1] - 100 * np.sin(yellow_track[2]))),
    #                 (255,0,0), 3)
    #         cv.line(frame, 
    #                 np.intp((blue_track[0] - 100 * np.cos(blue_track[2]), blue_track[1] + 100 * np.sin(blue_track[2]))),
    #                 np.intp((blue_track[0] + 100 * np.cos(blue_track[2]), blue_track[1] - 100 * np.sin(blue_track[2]))),
    #                 yellow_max, 3)
    # except:
    #         None

    cv.imshow('frame', frame)
    key = cv.waitKey(1)

    if key == ord('f'):
        break

    elif key == ord('p'):
        cv.waitKey(-1)

    # elif key == ord('r'):
    #     capture = cv.VideoCapture(video)