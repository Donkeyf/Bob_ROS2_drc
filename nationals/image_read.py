import cv2 as cv

def image_read(file):

    img = cv.imread(file)

    return img