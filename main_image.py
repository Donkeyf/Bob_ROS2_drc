import cv2 as cv
import numpy as np

from image_read import image_read
from colour_filter import colour_filter
from get_contours import get_contours
from contour_filters import contour_filter_4

yellow_min = (20, 100, 100)
yellow_max = (30, 255, 255)

blue_min = (90, 100, 100)
blue_max = (110, 255, 255)

# frame = image_read('indoor_track_image1.jpg')
frame = image_read('outdoor_track_image6.jpg')
frame_resize = cv.resize(frame, (128, 96))
# frame_resize = frame

# frame = image_read('outdoor_track_image1.jpg')
# frame_resize = cv.copyMakeBorder(frame_resize, 1, 1, 1, 1, cv.BORDER_CONSTANT)

blank_frame = np.zeros_like(frame_resize)
# blank_frame = cv.copyMakeBorder(blank_frame, 1, 1, 1, 1, cv.BORDER_CONSTANT)
# blank_frame = frame

frame_blur = frame_resize
# frame_blur = cv.GaussianBlur(frame_resize, (11,11), 1)
frame_yellow = colour_filter(frame_blur, yellow_min, yellow_max, 5, 5, 0)
frame_blue = colour_filter(frame_blur, blue_min, blue_max, 5, 5, 0)

contours_yellow = get_contours(frame_yellow)
contours_blue = get_contours(frame_blue)
# contours_yellow, yellow_track = contour_filter_4(contours_yellow)
# contours_blue, blue_track = contour_filter_4(contours_blue)

cv.drawContours(blank_frame, contours_yellow, -1, yellow_max)
cv.drawContours(blank_frame, contours_blue, -1, (255, 0, 0))

# try:
#         cv.line(blank_frame, 
#                 np.intp((yellow_track[0] - 100 * np.cos(yellow_track[2]), yellow_track[1] + 100 * np.sin(yellow_track[2]))),
#                 np.intp((yellow_track[0] + 100 * np.cos(yellow_track[2]), yellow_track[1] - 100 * np.sin(yellow_track[2]))),
#                 yellow_max, 3)
#         cv.line(blank_frame, 
#                 np.intp((blue_track[0] - 100 * np.cos(blue_track[2]), blue_track[1] + 100 * np.sin(blue_track[2]))),
#                 np.intp((blue_track[0] + 100 * np.cos(blue_track[2]), blue_track[1] - 100 * np.sin(blue_track[2]))),
#                 (255, 0, 0), 3)
# except:
#         None

cv.imshow('frame', blank_frame)
key = cv.waitKey(0)