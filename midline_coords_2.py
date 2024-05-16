import cv2 as cv
import numpy as np

def midline_coords(frame):

    coords = []

    frame = frame / 255

    xs = []
    ys = []

    threshold = 200
    trigger_y = False
    
    # print(len(frame[0]))
    
    for index, row in enumerate(frame):
        
        if sum(row) == 0:
            continue

        # Index counts from the bottom of the frame
        
        if index < 1/2 * len(frame):
            continue
        
        new_row = np.multiply(np.arange(len(row)),row)
        new_row = new_row[new_row != 0]

        # Insert extra filters here
        
        # if found != 0:
        #     # new_row = new_row[abs(new_row - prev_midpoint) < 20]
        #     if prev_index - index > 5:
        #         continue

        if len(new_row) > threshold:
            trigger_y = True
            break
        
        if len(new_row) == 0:
            continue

        midpoint = np.intp(sum(new_row) / len(new_row))
        
        coords.append((midpoint, index))

        # prev_index = index
        # found = 1

        xs.append(midpoint)
        ys.append(index)

    if trigger_y == False:
        coords = np.array(coords, dtype=np.float64)

        if len(xs) < 1:
            angle = None
            mid_x = 0
        else:
            slope = -np.polyfit(xs,ys,1)[0]
            angle = np.arctan(slope)

            if slope > 0:
                angle = np.pi/2 - angle
            elif slope < 0:
                angle = -np.pi/2 - angle

            angle = angle * 180 / np.pi

            mid_x = np.average(xs)

        return coords, angle, mid_x, False
    
    
    frame_t = frame.T

    coords = []

    frame_t = frame_t / 255

    xs = []
    ys = []

    for index, row in enumerate(frame_t):
        
        if sum(row) == 0:
            continue

        # Index counts from the bottom of the frame
        
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

        ys.append(midpoint)
        xs.append(index)    

    coords = np.array(coords, dtype=np.float64)
    
    if len(xs) < 1:
        angle = None
        mid_x = 0
    else:
        slope = -np.polyfit(xs,ys,1)[0]
        angle = np.arctan(slope)

        if slope > 0:
            angle = np.pi/2 - angle
        elif slope < 0:
            angle = -np.pi/2 - angle

        angle = -angle * 180 / np.pi

        mid_x = np.average(xs)

    return coords, angle, mid_x, True