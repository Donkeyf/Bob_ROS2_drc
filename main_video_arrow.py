import cv2 as cv
import numpy as np

from image_read import image_read
from colour_filter import colour_filter
from get_contours import get_contours
from contour_filters import contour_filter_1
from pinehsv_to_cvhsv import pinehsv_to_cvhsv
from midline_coords_3 import midline_coords_3

# Colours are in HSV
# Range is 0-180, 0-255, 0-255
# Range is 0-360, 0-100, 0-100 on https://pinetools.com/image-color-picker

pine_black_min = (0, 0, 0)
pine_black_max = (360, 100, 50)

black_min = pinehsv_to_cvhsv(pine_black_min)
black_max = pinehsv_to_cvhsv(pine_black_max)

capture = cv.VideoCapture(1)
capture.set(3, 128)
capture.set(4, 96)

while True:

    retval, frame = capture.read() 

    if not retval:
        break
    
    blank_frame = np.zeros_like(frame)

    frame_resize = frame
    frame_blur = frame_resize

    frame_black = colour_filter(frame_blur, black_min, black_max, 3, 5, 2)

    # black_mean_middle = midline_coords_3(frame_black)

    # if black_mean_middle != None:
        
    #     black_mean = black_mean_middle[0]
    #     black_middle = black_mean_middle[1]

    #     if (black_mean > black_middle):
    #         print('left', black_mean, black_middle)
    #     elif (black_mean < black_middle):
    #         print('right', black_mean, black_middle)

    edges = cv.Canny(frame_black,50,150,apertureSize = 3)
    contours_black, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contours_black = contour_filter_1(contours_black)

    cv.drawContours(frame, contours_black, -1, (0,0,255))

    
    if len(contours_black) != 0:        
        
        # Getting the contour which is hopefully the arrow
        
        cnt = contours_black[0]

        # Other criteria to determine if it is an arrow
        
        x,y,w,h = cv.boundingRect(cnt)
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        area = cv.contourArea(cnt)
        frame_black_invert = 255 - frame_black
        nonblack_mean, nonblack_middle = midline_coords_3(frame_black_invert, x, y, w, h)

        # Calculating and plotting middle point
        
        leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
        rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
        c_mid = int((rightmost[0] + leftmost[0]) / 2)

        cv.circle(frame, leftmost, radius=5, color=(255,0,0), thickness = 1)
        cv.circle(frame, rightmost, radius=5, color=(255,0,0), thickness = 1)
        
        # Calculating and plotting mean point

        M = cv.moments(cnt)
        # try:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])            
        
        cv.circle(frame, (cx, cy), radius=1, color=(0,255,0), thickness = 1)

        # Criteria to determine arrow
        
        if (cx > c_mid):
            if (nonblack_mean < nonblack_middle):
                if (cy < y + h/2):
                    if (w * h > 2 * area) & (w * h < 5 * area):
                        # print('left', cx, c_mid, nonblack_mean, nonblack_middle, cy, y + h/2)
                        print('left', area, w * h, w * h / area)
                    else:
                        print('nuh uh - not left - black to nonblack ratio is off')
                else:
                    print('nuh uh - not left - black too low')
            else:
                print('nuh uh - not left - nonblack mean is too right', cx, c_mid, nonblack_mean, nonblack_middle, cy, y + h/2)

        elif (cx < c_mid):
            if (nonblack_mean > nonblack_middle):
                if (cy < y + h/2):
                    if (w * h > 2 * area) & (w * h < 5 * area):
                        # print('right', cx, c_mid, nonblack_mean, nonblack_middle, cy, y + h/2)
                        print('right', area, w * h, w * h / area)
                    else:
                        print('nuh uh - not right - black to nonblack ratio is off')
                else:
                    print('nuh uh - not right - black too low')
            else:
                print('nuh uh - not right - nonblack mean is too left')
        else:
            print('nuh uh - not an arrow')

        # except:
        #     print('???')

    else:
        
        print('No black pixels detected')

    # contours_black = get_contours(frame_black)

    # Colour is in BGR
    
    cv.imshow('frame', frame)
    key = cv.waitKey(1)

    if key == ord('f'):
        break

    elif key == ord('p'):
        cv.waitKey(-1)

    # elif key == ord('r'):
    #     capture = cv.VideoCapture(video)