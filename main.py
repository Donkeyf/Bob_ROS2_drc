import cv2 as cv
import numpy as np
from monocular_VO import VisualOdometry

from midline_coords import midline_coords
from pinehsv_to_cvhsv import pinehsv_to_cvhsv
from colour_filter import colour_filter


def line_detection(frame):
    # Colours are in HSV

    # Range is 0-180, 0-255, 0-255
    yellow_min = (20, 100, 100)
    yellow_max = (30, 255, 255)

    # Colour for dilon webcam

    pine_blue_min = (190, 30, 70)
    pine_blue_max = (205, 100, 100)

    blue_min = pinehsv_to_cvhsv(pine_blue_min)
    blue_max = pinehsv_to_cvhsv(pine_blue_max)

    frame_blue = colour_filter(frame, blue_min, blue_max, 5, 5, 0)
    frame_yellow = colour_filter(frame, yellow_min, yellow_max, 5, 5, 0)

    blue_coords = midline_coords(frame_blue)
    yellow_coords = midline_coords(frame_yellow)

    return blue_coords, yellow_coords





def main():
    data_dir = "calibration"
    vo = VisualOdometry(data_dir)

    start_pose =  np.ones((3, 4))
    start_translation = np.zeros((3,1))
    start_rotation = np.identity(3)
    start_pose = np.concatenate((start_rotation, start_translation), axis = 1)
    curr_pose = start_pose

    bstart_pose =  np.ones((3, 4))
    bstart_translation = np.zeros((3,1))
    bstart_rotation = np.identity(3)
    bstart_pose = np.concatenate((bstart_rotation, bstart_translation), axis = 1)
    bcurr_pose = bstart_pose

    ystart_pose =  np.ones((3, 4))
    ystart_translation = np.zeros((3,1))
    ystart_rotation = np.identity(3)
    ystart_pose = np.concatenate((ystart_rotation, ystart_translation), axis = 1)
    ycurr_pose = ystart_pose

    capture = cv.VideoCapture(0)   
    capture.set(3, 128)
    capture.set(4, 96)

    old_frame = None
    new_frame = None

    bot_path = []
    b_pose = []
    y_pose = []

    prev_keys = 0

    b_pts_prev = []
    y_pts_prev = []

    mtx1 = 0


    i = 0
    while(capture.isOpened()):

        if(i == 0):
            ret, new_frame = capture.read()
            b_pts_prev, y_pts_prev = line_detection(new_frame)
            mtx1 = vo.P
            prev_keys = vo.process_first_frame(new_frame)
            old_frame = new_frame
            i += 1
            continue

        ret, new_frame = capture.read()
        prev_keys, transf, mtx2 = vo.process_frame(old_frame, new_frame, prev_keys)
        old_frame = new_frame

        curr_pose = np.matmul(curr_pose, np.linalg.inv(transf))
        bot_path.append((curr_pose[0, 3], 0, curr_pose[2, 3]))

        b_cur_pts, y_cur_pts = line_detection(new_frame)
        
        b_points_3D, y_points_3D = vo.triangulate(mtx1, mtx2, b_pts_prev, b_cur_pts, y_pts_prev, y_cur_pts)
        mtx1 = mtx2
        
        b_pts_prev = b_cur_pts
        y_pts_prev = y_cur_pts


        bcurr_pose = np.matmul(bcurr_pose, np.linalg.inv(b_points_3D))
        b_pose.append(bcurr_pose)

        ycurr_pose = np.matmul(ycurr_pose, np.linalg.inv(y_points_3D))
        y_pose.append(ycurr_pose)