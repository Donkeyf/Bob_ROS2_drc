import cv2 as cv
import numpy as np
from pinehsv_to_cvhsv import pinehsv_to_cvhsv
from colour_filter import colour_filter

def find_finish(pine_green_min, pine_green_max, frame_blur):
    green_min = pinehsv_to_cvhsv(pine_green_min)
    green_max = pinehsv_to_cvhsv(pine_green_max)

    frame_green = colour_filter(frame_blur, green_min, green_max, 5, 5, 0)

    line_green = cv.HoughLinesP(frame_green, 1, np.pi / 180, 160, None, 0, 0)


    if line_green is not None:
        
        x_sum = 0
        y_sum = 0

        for i in range(0, len(line_green)):
            theta = line_green[i][0][1]
            rho = line_green[i][0][0]
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
        return theta_double_avg / 2
    else:
        return  None