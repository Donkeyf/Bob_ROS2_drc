import cv2 as cv

def contour_rect_to_line(contours):

    total_area = 0
    total_x = 0
    total_y = 0
    total_angle = 0
    
    for contour in contours:

        total_area += cv.contourArea(contour)
        