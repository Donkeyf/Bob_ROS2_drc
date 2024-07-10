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
        
        elif blue_x == None and yellow_x != None:
            
            # If you don't see blue, go right
            
            if (yellow_x - centroid[0] < 60):
                return 0.6
            elif (yellow_x - centroid[0] < 180):
                return 1.2
            else:
                return None
            
        elif yellow_x == None and blue_x != None:
            
            # If you don't see yellow, go left
            
            if (centroid[0] - blue_x < 60):
                return 2.5
            elif (centroid[0] - blue_x < 180):
                return 1.9
            else:
                return None

        elif centroid[0] != None and blue_x == None and yellow_x == None:
            
            if centroid[0] < 160:
                return 1.2
            
            else:
                return 2.5

        else:
            
            # Go right
            
            if (yellow_x - centroid[0] < 60):
                return 0.6
            elif (yellow_x - centroid[0] < 130):
                return 1.2
            
            # Go left
            
            elif (centroid[0] - blue_x < 60):
                return 2.5
            elif (centroid[0] - blue_x < 130):
                return 1.9

if __name__ == '__main__':

    capture = cv2.VideoCapture(0)
    capture.set(3, 320)                         # Set Video Width to 320px
    capture.set(4, 240)                         # Set Video Height to 240px

    obs = ObstacleDetection(pine_purple_min, pine_purple_max)

    while True:
        retval, frame = capture.read() 

        cent = obs.obstacle_box(frame)
        print(cent)

        cv2.circle(frame, (cent), 5, (255, 0, 0), 5)


        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)

        if key == ord('f'):
            break

        elif key == ord('p'):
            cv2.waitKey(-1)