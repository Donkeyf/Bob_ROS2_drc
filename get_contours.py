import cv2 as cv
import numpy as np

def canny_threshold_values(img: cv.Mat, deviation: float=0.33) -> tuple[float, float]:  
    avgIntense = np.median(img)

    minVal = avgIntense * (1 - deviation)
    maxVal = avgIntense * (1 + deviation)

    return minVal, maxVal

def get_contours(frame):

    frame_y_min, frame_y_max = canny_threshold_values(frame)
    frame_y_canny = cv.Canny(frame, frame_y_min, frame_y_max)

    contours, _ = cv.findContours(frame_y_canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    return contours