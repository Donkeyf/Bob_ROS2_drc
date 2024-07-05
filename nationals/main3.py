import cv2 as cv
import numpy as np

from colour_filter import colour_filter
from midline_coords_2 import midline_coords
from pinehsv_to_cvhsv import pinehsv_to_cvhsv

from motor_control import MotorControl

from angle_controller import motor_speed

default_speed = 50

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


try:
    while True:
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
                rho = lines_blue[i][0][0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                # pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                # pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                # cv.line(frame_blur, pt1, pt2, (0,0,255), 1, cv.LINE_AA)
                x_sum = np.sin(2 * theta)
                y_sum = np.cos(2 * theta)
            
            theta_double_avg = np.angle(y_sum + x_sum * 1j)
            if theta_double_avg < 0:
                theta_double_avg = 2 * np.pi + theta_double_avg
            angle_blue = theta_double_avg / 2
            x0_blue = x0
            y0_blue = y0
        else:
            angle_blue = None
            x0_blue = None
            y0_blue = None

        if lines_yellow is not None:
            
            x_sum = 0
            y_sum = 0

            for i in range(0, len(lines_yellow)):
                theta = lines_yellow[i][0][1]
                rho = lines_yellow[i][0][0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                # pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                # pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                # cv.line(frame_blur, pt1, pt2, (0,0,255), 1, cv.LINE_AA)
                x_sum = np.sin(2 * theta)
                y_sum = np.cos(2 * theta)
            
            theta_double_avg = np.angle(y_sum + x_sum * 1j)
            if theta_double_avg < 0:
                theta_double_avg = 2 * np.pi + theta_double_avg
            angle_yellow = theta_double_avg / 2
            x0_yellow = x0
            y0_yellow = y0
        else:
            angle_yellow = None
            x0_yellow = None
            y0_yellow = None
        
        avg_speed = 50
        kp = 10

        if (angle_yellow == None) and (angle_blue == None):
            left_motor = avg_speed
            right_motor = avg_speed
        elif (angle_yellow != None) and (angle_blue == None):
            yellow_ref = 10 * np.pi / 180
            left_motor, right_motor = motor_speed(avg_speed, angle_yellow, yellow_ref, kp)

        elif (angle_yellow == None) and (angle_blue != None):
            blue_ref = np.pi - 10 * np.pi / 180
            left_motor, right_motor = motor_speed(avg_speed, angle_blue, blue_ref, kp)
        
        else:
            angle_x_sum = np.sin(2 * angle_yellow) + np.sin(2 * angle_blue)
            angle_y_sum = np.cos(2 * angle_yellow) + np.cos(2 * angle_blue)
            angle_double_average = np.angle(angle_y_sum + angle_x_sum * 1j)

            if angle_double_average < 0:
                angle_double_average = 2 * np.pi + angle_double_average
            
            angle_average = angle_double_average / 2

            if angle_average < 1.57:
                angle_average_ref = 0
            elif angle_average >= 1.57:
                angle_average_ref = 3.14

            left_motor, right_motor = motor_speed(avg_speed, angle_average, angle_average_ref, kp)

            

except KeyboardInterrupt:
    exit()