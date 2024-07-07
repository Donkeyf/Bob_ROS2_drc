import cv2 as cv
import numpy as np
from midline_coords_3 import midline_coords_3
from pinehsv_to_cvhsv import pinehsv_to_cvhsv
from colour_filter import colour_filter
from contour_filters import contour_filter_1

# Input the frame, it outputs: 'left', 'right', or 'None'

def arrow_detect_1(frame, pine_black_min, pine_black_max):

    # Put in the black colour
    
    black_min = pinehsv_to_cvhsv(pine_black_min)
    black_max = pinehsv_to_cvhsv(pine_black_max)

    # Filter out black
    
    frame_black = colour_filter(frame, black_min, black_max, 3, 5, 2)

    # Adds white border around the picture
    frame_black[:, 0] = 0
    frame_black[:, -1] = 0
    frame_black[0, :] = 0
    frame_black[-1, :] = 0

    # frame_black = cv.copyMakeBorder(frame_black, 5, 5, 5, 5, cv.BORDER_CONSTANT, None, value = 255)

    # Detect black edges
    
    edges = cv.Canny(frame_black,50,150,apertureSize = 3)
    contours_black, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours_black = contour_filter_1(contours_black)

    # If there is black detected
    
    if len(contours_black) != 0:        
        
        # Getting the contour which is hopefully the arrow
        
        cnt = contours_black[0]

        # Other criteria for checking if it is an arrow
        # Finding midpoints of non-black pixels
        
        x,y,w,h = cv.boundingRect(cnt)
        frame_black_invert = 255 - frame_black
        nonblack_mean, nonblack_middle = midline_coords_3(frame_black_invert, x, y, w, h)

        area = cv.contourArea(cnt)

        # Calculating middle and extreme points of black pixels
        
        leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
        rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
        c_mid = int((rightmost[0] + leftmost[0]) / 2)

        # Calculating and plotting mean point

        M = cv.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])            
        
        # Criteria to determine arrow
        
        if (cx > c_mid): # If mean black pixel is to the right of middle black pixel
            if (nonblack_mean < nonblack_middle): # If mean nonblack pixel is to the left of middle nonblack pixel
                if (cy < y + h/2): # If mean black pixel is above middle black pixel
                    if (w * h > 2 * area) & (w * h < 5 * area): # If arrow is between 1/5 and 1/2 area of bounding box
                        # print('left', cx, c_mid, nonblack_mean, nonblack_middle, cy, y + h/2)
                        return -0.6
            #         else:
            #             print('nuh uh - not left - black to nonblack ratio is off')
            #     else:
            #         print('nuh uh - not left - black too low')
            # else:
            #     print('nuh uh - not left - nonblack mean is too right', cx, c_mid, nonblack_mean, nonblack_middle, cy, y + h/2)

        elif (cx < c_mid):
            if (nonblack_mean > nonblack_middle):
                if (cy < y + h/2):
                    if (w * h > 2 * area) & (w * h < 5 * area):
                        # print('right', cx, c_mid, nonblack_mean, nonblack_middle, cy, y + h/2)
                        return 0.6
        #             else:
        #                 print('nuh uh - not right - black to nonblack ratio is off')
        #         else:
        #             print('nuh uh - not right - black too low')
        #     else:
        #         print('nuh uh - not right - nonblack mean is too left')
        # else:
        #     print('nuh uh - not an arrow')

        # except:
        #     print('???')

        else:
            return None

    else:
        
        return None
    
# Testing

if __name__ == '__main__':

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

        pine_black_min = (0, 0, 0)
        pine_black_max = (360, 100, 50)
        
        print(arrow_detect_1(frame, pine_black_min, pine_black_max))

        # # Adds white border around the picture
        # frame[:, 0] = 0
        # frame[:, -1] = 0
        # frame[0, :] = 0
        # frame[-1, :] = 0
        
        cv.imshow('frame', frame)
        key = cv.waitKey(1)

        if key == ord('f'):
            break

        elif key == ord('p'):
            cv.waitKey(-1)
