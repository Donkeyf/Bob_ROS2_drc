import cv2 as cv
import numpy as np

from image_read import image_read
from colour_filter import colour_filter
from get_contours import get_contours
from contour_filters import contour_filter_4

from midline_coords_2 import midline_coords
from pinehsv_to_cvhsv import pinehsv_to_cvhsv

from motor_control import MotorControl

default_speed = 40

pine_yellow_min = (30, 0, 60)
pine_yellow_max = (60, 100, 100)

pine_blue_min = (195, 30, 60)
pine_blue_max = (220, 100, 100)

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
        mc.change_speed(default_speed)

        retval, frame = capture.read() 

        if not retval:
            break
        
        blank_frame = np.zeros_like(frame)

        frame_resize = frame
        frame_blur = frame_resize
        frame_blue = colour_filter(frame_blur, blue_min, blue_max, 5, 5, 0)
        frame_yellow = colour_filter(frame_blur, yellow_min, yellow_max, 5, 5, 0)

        # Colour is in BGR

        blue_coords, blue_angle, blue_x = midline_coords(frame_blue)
        if len(blue_coords) == 0:
            True
        else:
            for point1, point2 in zip(blue_coords, blue_coords[1:]): 
                cv.line(frame, tuple(np.intp(point1)), tuple(np.intp(point2)), [0, 255, 255], 2) 

        yellow_coords, yellow_angle, yellow_x = midline_coords(frame_yellow)
        if len(yellow_coords) == 0:
            True
        else:
            for point1, point2 in zip(yellow_coords, yellow_coords[1:]): 
                cv.line(frame, tuple(np.intp(point1)), tuple(np.intp(point2)), [255, 0, 0], 2) 
        
        if (blue_angle != None) & (yellow_angle != None):
            angle = (blue_angle + yellow_angle) / 2
        elif (blue_angle == None) & (yellow_angle != None):
            angle = yellow_angle
        elif (blue_angle != None) & (yellow_angle == None):
            angle = blue_angle
        else:
            angle = 0

        print(angle)

        if (140 < yellow_x < 160):
            mc.course_correction(True)
        elif(160 < blue_x < 180):
            mc.course_correction(False)
        elif(angle < -10):
            mc.turn_left(angle)
        elif(angle > 10):
            mc.turn_right(angle)
        else:
            mc.change_speed(default_speed)
except KeyboardInterrupt:
    mc.stop()