import cv2
import numpy as np
img = cv2.imread('lena.bmp')
height = img.shape[0]
width = img.shape[1]
inv_img = img.copy()
for i in range(height):
	inv_img[height - 1 - i] = img[i]
cv2.imshow('My Image', inv_img)
cv2.waitKey(0)
