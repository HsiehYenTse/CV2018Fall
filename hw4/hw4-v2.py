import cv2
import numpy as np 
import sys

def reverseImage(img):
	outputimg = np.zeros((img.shape[0], img.shape[1]))
	for row in range(img.shape[0]):
		for col in range(img.shape[1]):
			if img[row][col] == 0:
				outputimg[row][col] = 255
			else:
				outputimg[row][col] = 0
	return outputimg

def convert2BinaryImage(img, mode=0):
	height = img.shape[0]
	width = img.shape[1]
	#convert grayscale into binary image, threshold is 128
	value = 255
	if mode == 1:
		value = 1
	for row in range(height):
		for col in range(width):
			pix = img[row][col]
			if pix >= 128:
				img[row][col] = value
			else:
				img[row][col] = 0
	return img

def BinaryDilation(img, kernel, anchor=(0, 0)):
	'''
	kernel is a matrix
	anchor is the start point of kernel
	'''
	height = img.shape[0]
	width = img.shape[1]
	outputimg = np.zeros((height, width))
	k_height = len(kernel)
	k_width = len(kernel[0])

	kernel_lst = []
	for row in range(k_height):
		for col in range(k_width):
			if kernel[row][col] != 0:
				kernel_lst.append((row-anchor[0], col-anchor[1]))
	#print(kernel_lst)
	
	for row in range(height):
		for col in range(width):
			if img[row][col] != 0:
				for n, i in enumerate(kernel_lst):
					if row+i[0] >= 0 and col+i[1] >= 0 and row+i[0] <= height-1 and col+i[1] <= width-1:
						outputimg[row+i[0]][col+i[1]] = 255
	return outputimg

def BinaryErosion(img, kernel, anchor=(0, 0)):

	height = img.shape[0]
	width = img.shape[1]
	outputimg = img.copy()
	k_height = len(kernel)
	k_width = len(kernel[0])

	kernel_lst = []
	for row in range(k_height):
		for col in range(k_width):
			if kernel[row][col] != 0:
				kernel_lst.append((row-anchor[0], col-anchor[1]))
	#print(kernel_lst)
	
	for row in range(height):
		for col in range(width):
			if img[row][col] != 0:
				for n, i in enumerate(kernel_lst):
					if row+i[0] < 0 or col+i[1] < 0 or row+i[0] > height-1 or col+i[1] > width-1:
						outputimg[row][col] = 0
					else:
						if img[row+i[0]][col+i[1]] == 0:
							outputimg[row][col] = 0

	return outputimg

def BinaryHit_Miss(img, reverseImg, Jkernel, Kkernel, Janchor, Kanchor):
	
	img1 = BinaryErosion(img, Jkernel, Janchor)
	img2 = BinaryErosion(reverseImg, Kkernel, Kanchor)
	outputimg = np.zeros((img.shape[0], img.shape[1]))
	for row in range(img.shape[0]):
		for col in range(img.shape[1]):
			if img1[row][col] == 255 and img2[row][col] == 255:
				outputimg[row][col] = 255
			else:
				outputimg[row][col] = 0
	
	return outputimg

	
def main(filename):
	img = cv2.imread(filename, 0)
	img = convert2BinaryImage(img)
	cv2.imwrite(filename+'_Binary.bmp', img)

	#cv2.imshow('image', img)
	#cv2.waitKey(0)
	#k = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
	k = [[0, 1, 1, 1, 0], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0]]
	anchor = (2, 2)

	reverseImg = reverseImage(img)
	cv2.imwrite(filename+'_reverse.bmp', reverseImg)


	
	outputimg1 = BinaryDilation(img, k, anchor)
	cv2.imwrite(filename+'_BinaryDilation.bmp', outputimg1)
	outputimg3 = BinaryErosion(outputimg1, k, anchor)
	cv2.imwrite(filename+'_Closing.bmp', outputimg3)


	outputimg2 = BinaryErosion(img, k, anchor)
	cv2.imwrite(filename+'_BinaryErosion.bmp', outputimg2)
	outputimg4 = BinaryDilation(outputimg2, k, anchor)
	cv2.imwrite(filename+'_Opening.bmp', outputimg4)
	
	Jkernel = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, 1, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
	Janchor = (2, 1)
	Kkernel = [[0, 0, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
	Kanchor = (2, 1)
	
	outputimg5 = BinaryHit_Miss(img, reverseImg, Jkernel, Kkernel, Janchor, Kanchor)
	cv2.imwrite(filename+'_Hit&Miss.bmp', outputimg5)
	

if __name__ == '__main__':

	try:
		filename = sys.argv[1]

	except IndexError:
		filename = 'lena.bmp'

	main(filename)
