import cv2
import numpy as np
img = cv2.imread('lena.bmp')
height = img.shape[0]
width = img.shape[1]
print(height, width)
inv_img = img.copy()
for i in range(height):
	for j in range(width):
		inv_img[height - 1 - i][width - 1 - j] = img[i][j]
cv2.imshow('My Image', inv_img)
cv2.waitKey(0)
