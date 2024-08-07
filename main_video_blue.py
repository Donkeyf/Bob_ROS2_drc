import cv2 as cv
import numpy as np

import math

from image_read import image_read
from colour_filter import colour_filter
from get_contours import get_contours
from contour_filters import contour_filter_4
from pinehsv_to_cvhsv import pinehsv_to_cvhsv
from angle_controller import motor_speed

# Colours are in HSV
# Range is 0-180, 0-255, 0-255

pine_blue_min = (40, 5, 70)
pine_blue_max = (60, 50, 100)

blue_min = pinehsv_to_cvhsv(pine_blue_min)
blue_max = pinehsv_to_cvhsv(pine_blue_max)

capture = cv.VideoCapture(0)
capture.set(3, 128)
capture.set(4, 96)

while True:

    retval, frame = capture.read() 

    if not retval:
        break
    
    blank_frame = np.zeros_like(frame)

    frame_resize = frame
    frame_blur = frame_resize
    frame_blur = cv.GaussianBlur(frame, (11,11), 100)

    frame_blue = colour_filter(frame_blur, blue_min, blue_max, 9, 5, 5)

    # # hist = cv.calcHist([frame_blue], [0], None, [256], [0, 256])
    # # print(hist)

    contours_blue = get_contours(frame_blue)

    cv.drawContours(blank_frame, contours_blue, -1, (255,255,255))
    
    
    # avgIntense = np.median(blank_frame)

    # minVal = avgIntense * (1 - 0.33)
    # maxVal = avgIntense * (1 + 0.33)
    # blank_frame = cv.Canny(blank_frame, minVal, maxVal)
    # print(blank_frame)
    
    # # Hough line
    
    lines = cv.HoughLines(frame_blue, 1, np.pi / 180, 160, None, 0, 0)
    
    # Draw the lines
    
    if lines is not None:
        
        theta_sum = 0
        x_sum = 0
        y_sum = 0

        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            # cv.line(frame_blur, pt1, pt2, (0,0,255), 1, cv.LINE_AA)
            theta_sum += theta
            x_sum = np.sin(2 * theta)
            y_sum = np.cos(2 * theta)
        
        # theta_avg = theta_sum / len(lines)
        
        theta_double_avg = np.angle(y_sum + x_sum * 1j)
        if theta_double_avg < 0:
            theta_double_avg = 2 * np.pi + theta_double_avg
        angle = theta_double_avg / 2

        a = math.cos(angle)
        b = math.sin(angle)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        
        cv.line(frame_blur, pt1, pt2, (255,0,0), 1, cv.LINE_AA)

        # a = math.cos(theta_avg)
        # b = math.sin(theta_avg)
        # x0 = a * rho
        # y0 = b * rho
        # pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        # pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

        # cv.line(frame_blur, pt1, pt2, (0,255,0), 1, cv.LINE_AA)

        # print(angle * 180 / np.pi)
        if angle < np.pi / 2:
            ref_angle = 0
        elif angle >= np.pi / 2:
            ref_angle = np.pi

        motor_speeds = motor_speed(50, angle, ref_angle, 10)
        print(motor_speeds[0], motor_speeds[1])
    
    cv.imshow('frame', frame_blur)
    key = cv.waitKey(1)

    if key == ord('f'):
        break

    elif key == ord('p'):
        cv.waitKey(-1)

    # elif key == ord('r'):
    #     capture = cv.VideoCapture(video)