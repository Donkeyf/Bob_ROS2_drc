import cv2 as cv
import numpy as np
from lib.visualization import plotting
import pickle
from matplotlib import pyplot as plt

from image_read import image_read
from colour_filter import colour_filter
from get_contours import get_contours
from contour_filters import contour_filter_4
from LK_mono_vis_odometry import VisualOdometry

def edge_detection(frame):
    # Colours are in HSV
    black_min = (0, 0, 0)
    black_max = (255, 255, 50)

    blank_frame = np.zeros_like(frame)
    frame_black = colour_filter(frame, black_min, black_max, 5, 5, 0)
    contours_black = get_contours(frame_black)
    cv.drawContours(frame, contours_black, -1, (0,0,255))
    cv.imshow('frame', frame)
    key = cv.waitKey(1)
    return contours_black



def main():


    estimated_path = []
    start_pose =  np.ones((3, 4))
    start_translation = np.zeros((3,1))
    start_rotation = np.identity(3)
    start_pose = np.concatenate((start_rotation, start_translation), axis = 1)



    capture = cv.VideoCapture(0)   
    capture.set(3, 128)
    capture.set(4, 96)
    
    data_dir = "camera_params"
    vo = VisualOdometry(data_dir)

    old_frame = None
    new_frame = None

    curr_pose = start_pose

    prev_keys = 0

    traj = np.zeros((600,600,3), dtype=np.uint8)

    i = 0

    while(capture.isOpened()):

        if(i == 0):
            ret, new_frame = capture.read()
            prev_keys = edge_detection(new_frame)
            old_frame = new_frame
            i += 1
            continue

        ret, new_frame = capture.read()
        new_keys = edge_detection(new_frame)
        prev_keys, transf = vo.process_frame(old_frame, new_frame, prev_keys, new_keys)
        old_frame = new_frame

        curr_pose = np.matmul(curr_pose, np.linalg.inv(transf))
        estimated_path.append((curr_pose[0, 3], curr_pose[2, 3]))
         
        if (i == 500):
            break

        i += 1

    cv.destroyAllWindows() 

    plotting.visualize_paths(estimated_path, estimated_path, "Visual Odometry", file_out="blah.html")

if __name__ == "__main__":
    main()