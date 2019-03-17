import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image
import imutils

image = cv2.imread('plate.jpg')
orig = image.copy()
image = imutils.resize(image, width=500)

# convert the image to grayscale, blur it, find edges in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 170, 200)
cv2.imshow('Outline', edged)
cv2.waitKey(0)

# find the contours
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
screenCnt = None

# loop over detected contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.025 * peri, True)
    if len(approx) == 4:    # found the contour with 4 points
        screenCnt = approx
        break

cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("Plate", image)
cv2.waitKey(0)