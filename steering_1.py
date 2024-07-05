import cv2 as cv
import numpy as np

import math

from image_read import image_read
from colour_filter import colour_filter
from get_contours import get_contours
from contour_filters import contour_filter_4
from pinehsv_to_cvhsv import pinehsv_to_cvhsv
from angle_controller import motor_speed

# import RPi.GPIO as gpio
# import time

# Colours are in HSV
# Range is 0-180, 0-255, 0-255

pine_yellow_min = (40, 5, 70)
pine_yellow_max = (60, 50, 100)

yellow_min = pinehsv_to_cvhsv(pine_yellow_min)
yellow_max = pinehsv_to_cvhsv(pine_yellow_max)

pine_blue_min = (190, 40, 50)
pine_blue_max = (220, 100, 100)

blue_min = pinehsv_to_cvhsv(pine_blue_min)
blue_max = pinehsv_to_cvhsv(pine_blue_max)

capture = cv.VideoCapture(0)
capture.set(3, 128)
capture.set(4, 96)

# # Pins: 

# # 27 - In 1 - Motor 1 - Green - Left
# p_in1 = 27
# # 17 - In 2 - Motor 1 - Yellow - Left
# p_in2 = 17
# # 24 - In 3 - Motor 2 - White furthest from green - Right
# p_in3 = 24
# # 23 - In 4 - Motor 2 - White closest to green - Right
# p_in4 = 23

# # 13 (pwm) - ENA - Motor 1 - Blue
# p_ena = 13
# # 12 (pwm) - ENB - Motor 2 - Purple 
# p_enb = 12

# max_speed = 100
# global_multiplier = 0.4

# def init():    
    
#     gpio.setwarnings(False) # The code is complaining too much
    
#     gpio.setmode(gpio.BCM)
#     gpio.setup(p_in1, gpio.OUT)
#     gpio.setup(p_in2, gpio.OUT)
#     gpio.setup(p_in3, gpio.OUT)
#     gpio.setup(p_in4, gpio.OUT)
    
#     gpio.setup(p_ena, gpio.OUT)
#     gpio.setup(p_enb, gpio.OUT)

# def change_speed_a(speed):
#     # print('Speed a: ', speed)
#     p_a.ChangeDutyCycle(speed)
# def change_speed_b(speed):
#     # print('Speed b: ', speed)
#     p_b.ChangeDutyCycle(speed)
# def setspeed(speed_a, speed_b):
#     p_a.ChangeDutyCycle(speed_a)
#     p_b.ChangeDutyCycle(speed_b)
# def setpins(pin_input):

#     if pin_input[0] == 'f':
#         gpio.output(p_in1, False)
#     elif pin_input[0] == 't':
#         gpio.output(p_in1, True)

#     if pin_input[1] == 'f':
#         gpio.output(p_in2, False)
#     elif pin_input[1] == 't':
#         gpio.output(p_in2, True)

#     if pin_input[2] == 'f':
#         gpio.output(p_in3, False)
#     elif pin_input[2] == 't':
#         gpio.output(p_in3, True)

#     if pin_input[3] == 'f':
#         gpio.output(p_in4, False)
#     elif pin_input[3] == 't':
#         gpio.output(p_in4, True)

# init()
# p_a = gpio.PWM(p_ena,global_multiplier * max_speed)
# p_b = gpio.PWM(p_enb,global_multiplier * max_speed)

# p_a.start(0)
# p_b.start(0)

# change_speed_a(0)
# change_speed_b(0)

# setpins('ftft')

while True:

    retval, frame = capture.read() 

    if not retval:
        break

    blank_frame = np.zeros_like(frame)

    frame_resize = frame
    frame_blur = frame_resize
    frame_blur = cv.GaussianBlur(frame, (11,11), 100)

    frame_blue = colour_filter(frame_blur, blue_min, blue_max, 9, 5, 5)
    frame_yellow = colour_filter(frame_blur, yellow_min, yellow_max, 9, 5, 5)

    lines_blue = cv.HoughLines(frame_blue, 1, np.pi / 180, 160, None, 0, 0)
    lines_yellow = cv.HoughLines(frame_yellow, 1, np.pi / 180, 160, None, 0, 0)

    if lines_blue is not None:
        
        x_sum = 0
        y_sum = 0

        # Extracting all the angles
        
        for i in range(0, len(lines_blue)):
            theta = lines_blue[i][0][1]
            rho = lines_blue[i][0][0]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            # pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            # pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            # cv.line(frame_blur, pt1, pt2, (0,255,0), 1, cv.LINE_AA)
            x_sum = np.sin(2 * theta)
            y_sum = np.cos(2 * theta)
        
        # Calculate the average angle
        
        theta_double_avg = np.angle(y_sum + x_sum * 1j)
        if theta_double_avg < 0:
            theta_double_avg = 2 * np.pi + theta_double_avg
        angle_blue = theta_double_avg / 2
        x0_blue = x0
        y0_blue = y0

        # Plot the best line
        
        a = math.cos(angle_blue)
        b = math.sin(angle_blue)
        pt1 = (int(x0_blue + 1000*(-b)), int(y0_blue + 1000*(a)))
        pt2 = (int(x0_blue - 1000*(-b)), int(y0_blue - 1000*(a)))
        cv.line(frame_blur, pt1, pt2, (0,255,0), 1, cv.LINE_AA)

    else:
        angle_blue = None
        x0_blue = None
        y0_blue = None

    if lines_yellow is not None:
        
        x_sum = 0
        y_sum = 0

        # Extracting all the angles
        
        for i in range(0, len(lines_yellow)):
            theta = lines_yellow[i][0][1]
            rho = lines_yellow[i][0][0]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            # pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            # pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            # cv.line(frame_blur, pt1, pt2, (0,0,255), 1, cv.LINE_AA)
            x_sum = np.sin(2 * theta)
            y_sum = np.cos(2 * theta)
        
        # Calculating average angle
        
        theta_double_avg = np.angle(y_sum + x_sum * 1j)
        if theta_double_avg < 0:
            theta_double_avg = 2 * np.pi + theta_double_avg
        angle_yellow = theta_double_avg / 2
        x0_yellow = x0
        y0_yellow = y0

        # Plot the best line
        
        a = math.cos(angle_yellow)
        b = math.sin(angle_yellow)
        pt1 = (int(x0_yellow + 1000*(-b)), int(y0_yellow + 1000*(a)))
        pt2 = (int(x0_yellow - 1000*(-b)), int(y0_yellow - 1000*(a)))
        cv.line(frame_blur, pt1, pt2, (0,0,255), 1, cv.LINE_AA)
    
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
        print(angle_yellow, angle_blue, angle_average)

    print(left_motor, right_motor)
    # setspeed(left_motor, right_motor)

    cv.imshow('frame', frame_blur)
    key = cv.waitKey(1)

    if key == ord('f'):
        break

    elif key == ord('p'):
        cv.waitKey(-1)