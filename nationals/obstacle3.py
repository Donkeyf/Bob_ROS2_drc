import cv2
import numpy as np
from colour_filter import colour_filter
from pinehsv_to_cvhsv import pinehsv_to_cvhsv

pine_purple_min = (270, 10, 25)
pine_purple_max = (330, 60, 100)

purple_min = pinehsv_to_cvhsv(pine_purple_min)
purple_max = pinehsv_to_cvhsv(pine_purple_max)

class ObstacleDetection:
    def __init__(self, pine_purple_min, pine_purple_max):
        self.purple_min = pinehsv_to_cvhsv(pine_purple_min)
        self.purple_max = pinehsv_to_cvhsv(pine_purple_max)
        
        self.width = 320
        self.height = 240

    def obstacle_box(self, frame):
        purple = colour_filter(frame, purple_min, purple_max)

        # Adds white border around the picture
        purple[:, 0] = 0
        purple[:, -1] = 0
        purple[0, :] = 0
        purple[-1, :] = 0

        contour, hierarchy = cv2.findContours(
        purple, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        if len(contour) == 0:
            return None
        
        max_area = 0
        for con in contour:
            area = cv2.contourArea(con)
            if area > max_area:
                max_area = area
                cnt = con

        
        # Calculating middle and extreme points of black pixels
        
        leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
        rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
        c_mid = int((rightmost[0] + leftmost[0]) / 2)

        # Calculating and plotting mean point

        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        return (cx, cy)
    
    def man_direction(self, centroid, blue_x, yellow_x):
        if (centroid[0] == None) and yellow_x == None and blue_x == None:
            return None
        
        elif blue_x == None:
            
            if (yellow_x - centroid[0] < 60):
                return -0.6
            elif (yellow_x - centroid[0] < 180):
                return -1.2
            else:
                return None
            
        elif yellow_x == None:
            if (centroid[0] - blue_x < 60):
                return 0.6
            elif (centroid[0] - blue_x < 180):
                return 1.2
            else:
                return None
            
        else:
            if (yellow_x - centroid[0] < 60):
                return -0.3
            elif (yellow_x - centroid[0] < 180):
                return -0.6
            elif (centroid[0] - blue_x < 60):
                return 0.3
            elif (centroid[0] - blue_x < 180):
                return 0.6
