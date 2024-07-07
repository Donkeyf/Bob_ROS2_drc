import cv2
import numpy as np


def detect_rectangles(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Debug: Show the result of edge detection
    cv2.imshow("Edges", edges)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 80, minLineLength=50, maxLineGap=20)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Rectangles Detected", image)
    cv2.waitKey(0)


capture = cv2.VideoCapture(0)
capture.set(3, 320)
capture.set(4, 240)

while True:
    retval, frame = capture.read()

    detect_rectangles(frame)

