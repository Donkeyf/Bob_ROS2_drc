import cv2 as cv
import numpy as np

from colour_filter import colour_filter
from get_contours import get_contours
from pinehsv_to_cvhsv import pinehsv_to_cvhsv

class ObstacleDetection:
    def __init__(self, pine_purple_min, pine_purple_max):
        self.purple_min = pinehsv_to_cvhsv(pine_purple_min)
        self.purple_max = pinehsv_to_cvhsv(pine_purple_max)
        
        self.width = 320
        self.height = 240
        
    def obstacle_box(self, frame):
        self.min_x = 2000
        self.max_x = 0
        self.min_y = 2000
        self.max_y = 0

        frame_purple = colour_filter(frame, self.purple_min, self.purple_max, 5, 5, 0)

        ctr = 0
        for row in frame:
            idx = 0
            while( idx < len(row)):
                if ((row[idx] > 0) and (idx < self.min_x)):
                    self.min_x = idx
                elif (row[idx] > 0 and idx > self.max_x):
                    self.max_x = idx

                if (row[idx] > 0 and ctr < self.min_y):
                    self.min_y = ctr
                elif(row[idx] > 0 and ctr > self.max_y):
                    self.max_y = ctr

                idx += 1
            ctr += 1

        centroid = ((self.max_x + self.min_x)/2 , (self.max_y, self.min_y)/2)
        height = self.max_y - self.min_y
        width = self.max_x - self.min_x

        return centroid, width, height
    
    def man_direction(self, centroid, blue_x, yellow_x):
        if (centroid - blue_x < 60):
            return 20
        elif (centroid - blue_x < 180):
            return 40
        elif (yellow_x - centroid < 60):
            return -20
        elif (yellow_x - centroid < 180):
            return -40
        else:
            return None


    