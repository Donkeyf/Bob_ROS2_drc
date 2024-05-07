import cv2 as cv
import numpy as np

def midline_coords(frame):

    coords = []

    frame = frame / 255
    found = 0
    
    # print(len(frame[0]))
    
    for index, row in enumerate(frame):

        if sum(row) == 0:
            continue

        new_row = np.multiply(np.arange(len(row)),row)
        new_row = new_row[new_row != 0]

        # Insert extra filters here
        
        # if found != 0:
        #     # new_row = new_row[abs(new_row - prev_midpoint) < 20]
        #     if prev_index - index > 5:
        #         continue

        if len(new_row) == 0:
            continue

        midpoint = np.intp(sum(new_row) / len(new_row))
        
        coords.append((midpoint, index))

        # prev_index = index
        # found = 1

    coords = np.array(coords)

    return coords

