import cv2
import numpy as np
from colour_filter import colour_filter
from pinehsv_to_cvhsv import pinehsv_to_cvhsv

pine_purple_min = (270, 10, 25)
pine_purple_max = (330, 60, 100)

purple_min = pinehsv_to_cvhsv(pine_purple_min)
purple_max = pinehsv_to_cvhsv(pine_purple_max)

def detect_rectangles(image):

    # frame_blur = image
    frame_blur = cv2.GaussianBlur(image, (11,11), 100)

    purple = colour_filter(frame_blur, purple_min, purple_max)
    # gray = cv2.cvtColor(purple, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(purple, 50, 150, apertureSize=3)

    # # Debug: Show the result of edge detection
    # cv2.imshow("Edges", edges)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 80, minLineLength=50, maxLineGap=20)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return image


capture = cv2.VideoCapture(1)
capture.set(3, 320)
capture.set(4, 240)

while True:
    retval, frame = capture.read()

    image = detect_rectangles(frame)

    cv2.imshow("Rectangles Detected", image)
    key = cv2.waitKey(1)

    if key == ord('f'):
        break

    elif key == ord('p'):
        cv2.waitKey(-1)