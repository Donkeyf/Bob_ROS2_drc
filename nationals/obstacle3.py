import cv2
import numpy as np
from colour_filter import colour_filter
from pinehsv_to_cvhsv import pinehsv_to_cvhsv

pine_purple_min = (270, 10, 25)
pine_purple_max = (330, 60, 100)

purple_min = pinehsv_to_cvhsv(pine_purple_min)
purple_max = pinehsv_to_cvhsv(pine_purple_max)


capture = cv2.VideoCapture(0)
capture.set(3, 320)
capture.set(4, 240)

while True:
    retval, frame = capture.read()

    # Read the input image
    input_image = frame
    original_image = input_image.copy()

    frame_blur = cv2.GaussianBlur(frame, (11,11), 100)

    purple = colour_filter(frame_blur, purple_min, purple_max)
    grayscale_image = cv2.cvtColor(purple, cv2.COLOR_BGR2GRAY)

    # Convert to binary image
    _, binary_image = cv2.threshold(grayscale_image, 150, 255, cv2.THRESH_BINARY)

    # Find all the contours
    all_contours, hierarchy = cv2.findContours(
        binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )

    # Loop through individual contours
    for contour in all_contours:
        # Approximate contour to a polygon
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        # Calculate aspect ratio and bounding box
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h

            # Draw bounding box
            cv2.drawContours(original_image, [approx], -1, (0, 255, 0), 3)
            cv2.putText(
                original_image,
                "Rectangle",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    # Display the result
    cv2.imshow("Detected Rectangles", original_image)
    key = cv2.waitKey(1)

    if key == ord('f'):
        break

    elif key == ord('p'):
        cv2.waitKey(-1)