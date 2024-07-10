import cv2 as cv
import numpy as np
from pinehsv_to_cvhsv import pinehsv_to_cvhsv
from colour_filter import colour_filter

pine_black_min = (80, 0, 0)
pine_black_max = (130, 100, 40)

def arrow_detect_1(pine_black_min, pine_black_max, frame_blur):
    black_min = pinehsv_to_cvhsv(pine_black_min)
    black_max = pinehsv_to_cvhsv(pine_black_max)

    frame_black = colour_filter(frame_blur, black_min, black_max, 5, 5, 0)

    line_black = cv.HoughLines(frame_black, 1, np.pi / 180, 160, None, 0, 0)

    if line_black is not None:
        x_sum = 0
        y_sum = 0
        theta_black_list = []

        #math to find line position
        for i in range(0, len(line_black)):
            theta = line_black[i][0][1]
    
            if theta > np.pi / 2:
                theta_black_list.append(theta - np.pi)
            else:
                theta_black_list.append(theta)

            rho = line_black[i][0][0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x_sum = np.sin(2 * theta)
            y_sum = np.cos(2 * theta)
        
        theta_double_avg = np.angle(y_sum + x_sum * 1j)
        if theta_double_avg < 0:
            theta_double_avg = 2 * np.pi + theta_double_avg
        angle_black = theta_double_avg / 2

        if (angle_black < 70 * np.pi / 180) or (angle_black > 110 * np.pi / 180):
            theta_black_list = np.sort(theta_black_list)
            theta_black_list_remove = theta_black_list[:int(len(theta_black_list) / 2) + 1]
            angle_black = np.average(theta_black_list_remove)
            if angle_black < 0:
                angle_black = angle_black + np.pi

    return angle_black

