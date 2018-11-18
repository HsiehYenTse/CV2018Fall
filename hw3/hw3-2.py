import cv2
import numpy as np
from matplotlib import pyplot as plt
def histogram_equalization(img):
	size = img.shape[0] * img.shape[1]
	sum = 0
	hist_img = histogram(img)

	'''
	for i in range(len(hist_img)):
		sum += hist_img[i]/size
		hist_img[i] = int(255 * sum)
	'''
	hist_img = list(map(lambda x : sum(hist_img[:x])*255/size, hist_img))

	for row in range(img.shape[0]):
		for col in range(img.shape[1]):
			img[row][col] = hist_img[img[row][col]]
	return img

def histogram(img):
	hist_img = [0] * 256
	for row in range(img.shape[0]):
		for col in range(img.shape[1]):
			pix = img[row][col]
			hist_img[pix] += 1
	return hist_img


if __name__ == '__main__':

	FileName = 'lena.bmp'

	img = cv2.imread(FileName, cv2.IMREAD_GRAYSCALE)
	img_HisEq = histogram_equalization(img)
	#cv2.imshow(img)
	cv2.imwrite(FileName+'_HistogramEquli.bmp', img_HisEq)


	
