# Configuration Parameters for Motor Control and Object Detection
DEFAULT_SPEED = 40
ARROW_MULTIPLIER = 1.5
OBJECT_MULTIPLIER = 1

# PID Controller Gains
KP = 70
KI = 0
KD = 40

# # Configuration Parameters for Motor Control and Object Detection
# DEFAULT_SPEED = 100
# ARROW_MULTIPLIER = 1.5
# OBJECT_MULTIPLIER = 1

# # PID Controller Gains
# KP = 25
# KI = 0
# KD = 0

import cv2 as cv
import numpy as np

from colour_filter import colour_filter
from midline_coords_2 import midline_coords
from pinehsv_to_cvhsv import pinehsv_to_cvhsv

from motor_control_2 import MotorControl
from angle_controller import motor_speed
from angle_controller_2 import pid_motor_speed
from arrow_detect_1 import arrow_detect_1
from start_stop import find_finish

import RPi.GPIO as gpio

import time

from obstacle3 import ObstacleDetection

start_time = time.time()

pine_yellow_min = (40, 5, 50)
pine_yellow_max = (55, 100, 100)

pine_blue_min = (185, 20, 60)
pine_blue_max = (220, 100, 100)

pine_black_min = (0, 0, 0)
pine_black_max = (360, 100, 50)

pine_purple_min = (270, 10, 25)
pine_purple_max = (330, 60, 100)

pine_green_min = (55, 19, 50)
pine_green_max = (70, 45, 90)

yellow_min = pinehsv_to_cvhsv(pine_yellow_min)
yellow_max = pinehsv_to_cvhsv(pine_yellow_max)

blue_min = pinehsv_to_cvhsv(pine_blue_min)
blue_max = pinehsv_to_cvhsv(pine_blue_max)

# Video Capture Setup
capture = cv.VideoCapture(0)
capture.set(3, 320)                         # Set Video Width to 320px
capture.set(4, 240)                         # Set Video Height to 240px

# Initialise Motor Controller and Obstacle Detection
mc = MotorControl()
obs = ObstacleDetection(pine_purple_min, pine_purple_max)

#set motors to go forward
mc.setpins('ftft')

#initial timestep
previous_time = time.time()
previous_error = 0
current_integral = 0

try:
    while True:
        retval, frame = capture.read() 

        frame_fresh = frame.copy()
        frame = frame[int(len(frame)/2):int(len(frame))]
        frame_blur = cv.GaussianBlur(frame, (11,11), 100)
        frame_fresh_blur = cv.GaussianBlur(frame_fresh, (11,11), 100)

        frame_blue = colour_filter(frame_blur, blue_min, blue_max, 5, 5, 0)
        frame_yellow = colour_filter(frame_blur, yellow_min, yellow_max, 5, 5, 0)

        #find the lines for the lanes
        lines_blue = cv.HoughLines(frame_blue, 1, np.pi / 180, 160, None, 0, 0)
        lines_yellow = cv.HoughLines(frame_yellow, 1, np.pi / 180, 160, None, 0, 0)

        if lines_blue is not None:
            x_sum = 0
            y_sum = 0

            #math to find line position
            for i in range(0, len(lines_blue)):
                theta = lines_blue[i][0][1]
                rho = lines_blue[i][0][0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
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

        # print(angle_yellow, x0_yellow, y0_yellow)
        cent = obs.obstacle_box(frame)
        if cent == None:
            ob_angle = None
        elif x0_blue != None or x0_yellow != None:
            ob_angle = obs.man_direction(cent, x0_blue, x0_yellow)
        else:
            ob_angle = 1.2
        
        arrow_angle = None
        #detect arrow
        # arrow_angle = arrow_detect_1(frame_fresh_blur, pine_black_min, pine_black_max)

        #look for finish line
        finish_angle = None
        if time.time() - start_time > 3:
            finish_angle = find_finish(pine_green_min, pine_green_max, frame_blur)


        if (arrow_angle != None):
            arrow_angle = arrow_angle * ARROW_MULTIPLIER
            left_motor, right_motor, previous_time, previous_error, current_integral \
                = pid_motor_speed(DEFAULT_SPEED, arrow_angle, 0, previous_time, previous_error, current_integral, KP, KI, KD)
            
            print('arrow', left_motor, right_motor, arrow_angle)
            mc.change_speed(left_motor, right_motor)
            time.sleep(0.5)

        elif (ob_angle != None):
            ob_angle = ob_angle * OBJECT_MULTIPLIER
            left_motor, right_motor, previous_time, previous_error, current_integral \
                = pid_motor_speed(DEFAULT_SPEED, ob_angle, 0, previous_time, previous_error, current_integral, KP, KI, KD)
            print('obstacle', left_motor, right_motor)
            mc.change_speed(left_motor, right_motor)
        
        elif (finish_angle != None):
            left_motor, right_motor, previous_time, previous_error, current_integral \
                = pid_motor_speed(DEFAULT_SPEED, finish_angle, np.pi/2, previous_time, previous_error, current_integral, KP, KI, KD)

            print('Finish', left_motor, right_motor)
            mc.change_speed(0, 0)
            exit()

        elif (angle_yellow == None) and (angle_blue == None):
            left_motor = DEFAULT_SPEED
            right_motor = DEFAULT_SPEED

            _, _, previous_time, previous_error, current_integral \
                = pid_motor_speed(DEFAULT_SPEED, 0, 0, previous_time, previous_error, current_integral, KP, KI, KD)

            print('none', left_motor, right_motor)
            mc.change_speed(left_motor, right_motor)

        elif (angle_yellow != None) and (angle_blue == None):
            yellow_ref = 10 * np.pi / 180
            left_motor, right_motor, previous_time, previous_error, current_integral \
                = pid_motor_speed(DEFAULT_SPEED, angle_yellow, yellow_ref, previous_time, previous_error, current_integral, KP, KI, KD)

            print('yellow', left_motor, right_motor)
            mc.change_speed(left_motor, right_motor)

        elif (angle_yellow == None) and (angle_blue != None):
            blue_ref = np.pi - 10 * np.pi / 180
            left_motor, right_motor, previous_time, previous_error, current_integral \
                = pid_motor_speed(DEFAULT_SPEED, angle_blue, blue_ref, previous_time, previous_error, current_integral, KP, KI, KD)

            print('blue', left_motor, right_motor)
            mc.change_speed(left_motor, right_motor)

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

            left_motor, right_motor, previous_time, previous_error, current_integral \
                = pid_motor_speed(DEFAULT_SPEED, angle_average, angle_average_ref, previous_time, previous_error, current_integral, KP, KI, KD)


            print('both', left_motor, right_motor)
            mc.change_speed(left_motor, right_motor)

except KeyboardInterrupt:
    gpio.cleanup()