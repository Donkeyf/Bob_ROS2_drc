import cv2 as cv
import numpy as np

def contour_filter_1(contours):

    # This will remove contours that are less than half the maximum sized contour or less than 100
    
    contours_list = list(contours)
    
    contours_list = [contour for contour in contours_list if cv.contourArea(contour) > 100]

    current_max = 0
    for contour in contours_list:
        if (cv.contourArea(contour) > current_max):
            current_max = cv.contourArea(contour)

    contours_list = [contour for contour in list(contours) if cv.contourArea(contour) > current_max / 2]

    contours_filtered = tuple(contours_list)

    return contours_filtered

def contour_filter_2(contours):

    # This will remove contours that are less than 100 and approximate them as polygons
    
    contours_list = list(contours)
    
    contours_list = [contour for contour in contours_list if cv.contourArea(contour) > 100]

    contours_list = [cv.approxPolyDP(contour, 0.02*cv.arcLength(contour, True),True) for contour in contours_list]

    contours_filtered = tuple(contours_list)

    return contours_filtered

def contour_filter_3(contours):

    # This will remove contours that are less than 100 and approximate them as rectangles
    
    contours_list = list(contours)
    
    contours_list = [contour for contour in contours_list if cv.contourArea(contour) > 100]

    contours_list = [np.int0(cv.boxPoints(cv.minAreaRect(contour))) for contour in contours_list]

    contours_filtered = tuple(contours_list)

    return contours_filtered

def contour_filter_4(contours):

    # This will remove contours that are less than 100 and approximate them as rectangles which get turned into lines
    
    
    contours_list = list(contours)
    
    # contours_list = [contour for contour in contours_list if cv.contourArea(contour) > 30]

    if len(contours_list) < 1:
        return contours, None

    contours_list_final = []

    total_area = 0
    total_angle_weight = 0
    total_x_weight = 0
    total_y_weight = 0
    
    for contour in contours_list:

        rect = cv.minAreaRect(contour)

        width = rect[1][0]
        height = rect[1][1]
        angle = rect[2]
        centre_x = rect[0][0]
        centre_y = rect[0][1]
        area = width * height

        if angle > 89.9 or (-0.1 < angle < 0.1):
            true_angle = 90
        elif height > width:
            # if angle > 0:
            #     angle = -angle
            
            true_angle = 90 - angle
        else:
            # if angle > 0:
            #     angle = -angle
            true_angle = 180 - angle

        total_area += area
        total_angle_weight += area * true_angle
        total_x_weight += area * centre_x
        total_y_weight += area * centre_y
        
        box = np.int0(cv.boxPoints(rect))
        contours_list_final.append(box)
        print(height, width, centre_y, angle, true_angle)

    overall_angle_deg = total_angle_weight / total_area
    overall_angle = overall_angle_deg * np.pi / 180
    overall_x = total_x_weight / total_area
    overall_y = total_y_weight / total_area

    rect_coords = (overall_x, overall_y, overall_angle) # ANGLE OUTPUTS IN RADIANS
    print(rect_coords)

    contours_filtered = tuple(contours_list_final)

    return contours_filtered, rect_coords