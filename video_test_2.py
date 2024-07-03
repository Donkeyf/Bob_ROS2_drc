import cv2 as cv

# https://pinetools.com/image-color-picker

# We want 0-180, 0-255, 0-255
# But get 0-360, 0-100, 0-100 on pinetools

capture = cv.VideoCapture(1)

while True:

    retval, frame = capture.read() 

    if not retval:
        break

    frame = cv.GaussianBlur(frame, (11,11), 10)

    cv.imshow('frame', frame)
    key = cv.waitKey(1)

    if key == ord('f'):
        break

    elif key == ord('p'):
        cv.waitKey(-1)