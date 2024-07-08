import cv2 as cv
import numpy as np

def midline_coords_3(frame, x, y, w, h):

    coords = []

    frame = frame / 255

    xs = np.array([])
    ys = []

    frame_y = len(frame)

    for index, row in enumerate(frame):
        
        if sum(row) == 0:
            continue

        if (index > frame_y - y) or (index < frame_y - y - h):
            continue

        for column_index, column in enumerate(row):
            if (column_index < x) or (column_index > x + w):
                row[column_index] = 0

        # Index counts from the bottom of the frame
        
        new_row = np.multiply(np.arange(len(row)),row)
        new_row = new_row[new_row != 0]
        
        if len(new_row) == 0:
            continue

        xs = np.concatenate((xs, new_row))

    if len(xs) > 0:
        mean = np.mean(xs)
        middle = (np.max(xs) + np.min(xs)) / 2

        return mean, middle
    
    else:
        return 0, 0