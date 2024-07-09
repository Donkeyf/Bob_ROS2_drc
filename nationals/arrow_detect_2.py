import cv2 as cv
import numpy as np

capture = cv.VideoCapture(0)
capture.set(3, 320)                         # Set Video Width to 320px
capture.set(4, 240)                         # Set Video Height to 240px


while True:
    ret, img = capture.read()
    src = np.float32([[0, 240], [1207, 240], [0, 0], [320, 0]])
    dst = np.float32([[569, 240], [711, 240], [0, 0], [320, 0]])
    M = cv.getPerspectiveTransform(src, dst) # The transformation matrix
    Minv = cv.getPerspectiveTransform(dst, src) # Inverse transformation

    img = img[450:(450+240), 0:320] # Apply np slicing for ROI crop
    warped_img = cv.warpPerspective(img, M, (320, 240)) # Image warping

    cv.imshow('frame', warped_img)
    key = cv.waitKey(1)

    if key == ord('f'):
        break

    elif key == ord('p'):
        cv.waitKey(-1)
