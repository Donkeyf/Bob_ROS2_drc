import cv2 as cv
import time as time

# https://pinetools.com/image-color-picker

# We want 0-180, 0-255, 0-255
# But get 0-360, 0-100, 0-100 on pinetools

capture = cv.VideoCapture(0)
capture.set(3, 320)                         # Set Video Width to 320px
capture.set(4, 240)                         # Set Video Height to 240px

while True:

    retval, frame = capture.read() 

    frame = cv.GaussianBlur(frame, (11,11), 100)

    if not retval:
        break

    cv.imshow('frame', frame)
    key = cv.waitKey(1)

    if key == ord('f'):
        break

    elif key == ord('a'):
        name = 'nationals/training_photos_left/a_' + str(time.time()) + '.png'
        cv.imwrite(name, frame)
        # break

    elif key == ord('d'):
        name = 'nationals/training_photos_right/d_' + str(time.time()) + '.png'
        cv.imwrite(name, frame)

    elif key == ord('p'):
        cv.waitKey(-1)