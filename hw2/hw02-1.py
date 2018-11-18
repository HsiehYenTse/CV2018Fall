import cv2
import numpy as np
import matplotlib.pyplot as plt

#以灰階讀入圖片; 0代表cv2.IMREAD_GRAYSCALE, 1代表cv2.IMREAD_COLOR, 
#			  -1代表cv2.IMREAD_UNCHANGED

FileName = 'lena.bmp'
img = cv2.imread(FileName, 0)
#print(img.shape)
hist_img = [0] *256
#print(hist_img)

for col in range(img.shape[0]):
	for row in range(img.shape[1]):
		pix = img[col][row]
		hist_img[pix] += 1
		if pix >= 128:
			img[col][row] = 255
		else:
			img[col][row] = 0
#print(len(hist_img))
plt.bar(range(len(hist_img)), hist_img, width = 4)
plt.show()

cv2.imwrite('BinaryImage_' + FileName, img)



#cv2.imshow('image', img)
#cv2.waitKey(0)