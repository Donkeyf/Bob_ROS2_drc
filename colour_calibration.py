import cv2 as cv

# https://pinetools.com/image-color-picker

# We want 0-180, 0-255, 0-255
# But get 0-360, 0-100, 0-100 on pinetools

capture = cv.VideoCapture(0)

while True:

    retval, frame = capture.read() 

    if not retval:
        break

    cv.imshow('frame', frame)
    key = cv.waitKey(1)

    if key == ord('f'):
        break

    if key == ord('c'):
        name = 'colour.png'
        cv.imwrite(name, frame)
        break

    elif key == ord('p'):
        cv.waitKey(-1)