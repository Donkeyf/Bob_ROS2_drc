import cv2 as cv
import numpy as np

from colour_filter import colour_filter
from midline_coords_2 import midline_coords
from pinehsv_to_cvhsv import pinehsv_to_cvhsv

from motor_control import MotorControl

from obstacle import ObstacleDetection

default_speed = 30

pine_yellow_min = (20, 5, 60)
pine_yellow_max = (60, 100, 100)

pine_blue_min = (195, 30, 60)
pine_blue_max = (220, 100, 100)

pine_black_min = (0, 0, 0)
pine_black_max = (360, 100, 50)

pine_purple_min = (310, 20, 40)
pine_purple_max = (370, 50, 70)

yellow_min = pinehsv_to_cvhsv(pine_yellow_min)
yellow_max = pinehsv_to_cvhsv(pine_yellow_max)

blue_min = pinehsv_to_cvhsv(pine_blue_min)
blue_max = pinehsv_to_cvhsv(pine_blue_max)

capture = cv.VideoCapture(0)
capture.set(3, 320)
capture.set(4, 240)

mc = MotorControl()
mc.forward()

try:
    while True:
        mc.change_speed()
        retval, frame = capture.read() 


        if not retval:
            break
        
        blank_frame = np.zeros_like(frame)
        frame_blur = cv.GaussianBlur(frame, (11,11), 100)

        frame_blue = colour_filter(frame_blur, blue_min, blue_max, 5, 5, 0)
        frame_yellow = colour_filter(frame_blur, yellow_min, yellow_max, 5, 5, 0)

        lines_blue = cv.HoughLines(frame_blue, 1, np.pi / 180, 160, None, 0, 0)
        lines_yellow = cv.HoughLines(frame_yellow, 1, np.pi / 180, 160, None, 0, 0)

        if lines_blue is not None:
            
            x_sum = 0
            y_sum = 0

            for i in range(0, len(lines_blue)):
                theta = lines_blue[i][0][1]
                # rho = lines[i][0][0]
                # a = math.cos(theta)
                # b = math.sin(theta)
                # x0 = a * rho
                # y0 = b * rho
                # pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                # pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                # cv.line(frame_blur, pt1, pt2, (0,0,255), 1, cv.LINE_AA)
                x_sum = np.sin(2 * theta)
                y_sum = np.cos(2 * theta)
            
            theta_double_avg = np.angle(y_sum + x_sum * 1j)
            if theta_double_avg < 0:
                theta_double_avg = 2 * np.pi + theta_double_avg
            angle_blue = theta_double_avg / 2
        else:
            angle_blue = None

        if lines_yellow is not None:
            
            x_sum = 0
            y_sum = 0

            for i in range(0, len(lines_yellow)):
                theta = lines_yellow[i][0][1]
                # rho = lines[i][0][0]
                # a = math.cos(theta)
                # b = math.sin(theta)
                # x0 = a * rho
                # y0 = b * rho
                # pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                # pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                # cv.line(frame_blur, pt1, pt2, (0,0,255), 1, cv.LINE_AA)
                x_sum = np.sin(2 * theta)
                y_sum = np.cos(2 * theta)
            
            theta_double_avg = np.angle(y_sum + x_sum * 1j)
            if theta_double_avg < 0:
                theta_double_avg = 2 * np.pi + theta_double_avg
            angle_yellow = theta_double_avg / 2
        else:
            angle_yellow = None       

except KeyboardInterrupt:
    mc.stop()