import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def convert2BinaryImage(img):
	height = img.shape[0]
	width = img.shape[1]
	#convert grayscale into binary image, threshold is 128
	for row in range(height):
		for col in range(width):
			pix = img[row][col]
			if pix >= 128:
				img[row][col] = 255
			else:
				img[row][col] = 0
	return img


def Connected_Components(img):
	'''
	img_label:shape與img相同的2D.list，目的是要存放每個像素對應到label編號
	labels:  ex.[0, 1, 2, 3, 4, 5, 6, ...]
			 ex.label4, label5連通=>[0, 1, 2, 3, 5, 5, 6]
	labels主要就是拿來存放標籤的變化結果，位置代表原本的標籤號碼
	位置對應的值代表後來經過聯通後的標籤號碼
	演算法步驟：（從左上至右下掃描每一個pixel）
	1.當pixel的值！＝0，則
	2-a.去判斷左邊的pixel是否!=0，若!=0，則
	    把目前pixel的img_label存成左邊的pixel的標籤號碼
	2-b.去判斷左邊的pixel是否!=0，若==0，則
	    把目前pixel的img_label存成新的一個標籤號碼
	3-a.去判斷上方的pixel是否!=0，若!=0，則
	    把labels中所有的element的值跟上方pixel的img_label相同的element
	    改成目前pixel的img_label值
	4.第二次掃瞄，由img_label與labels
	  img_label[i] = labels[ img_label[i] ]   
	'''

	height = img.shape[0]
	width = img.shape[1]
	img_label = [ [-1]*width for h in range(height) ]		
	labels = [0]	
	#轉換成0, 1的標籤
	for row in range(height):
		for col in range(width):
			if img[row][col] == 0:
				img[row][col] = 0
			else:
				img[row][col] = 1
    #第一次掃瞄
	for row in range(height):
		for col in range(width):
			if img[row][col] != 0:
				img_label[row][col] = labels[-1]	
				if col > 0:
					if img[row][col-1] != 0:
						img_label[row][col] = img_label[row][col-1]
					else:
						labels.append(labels[len(labels)-1]+1)
						img_label[row][col] = labels[-1]
                        
				if row > 0:
					if img_label[row-1][col] != -1 and labels[img_label[row-1][col]] != labels[-1]:
						temp = labels[img_label[row-1][col]]
						for n, i in enumerate(labels):
							if i == temp:
								labels[n] = labels[-1]
		labels.append(labels[len(labels)-1]+1)
	#第二次掃瞄
	for row in range(height):
		for col in range(width):
			if img_label[row][col] != -1:
				img_label[row][col] = labels[img_label[row][col]]
	
	bin_list = list(set(labels))
	return img_label, bin_list

def find_regionPoint(img_bin, bin_list, target_value):
	height = len(img_bin)
	width = len(img_bin[0])
	bin_count = [0] * len(bin_list)
	for row in range(height):
		for col in range(width):
			if img_bin[row][col] != -1:
				bin_count[bin_list.index(img_bin[row][col])] += 1

	target_label = []
	#print the label that the region is more than 500pix 
	for n, i in enumerate(bin_count):
		if i > target_value:
			target_label.append(bin_list[n])

	top = [height] * len(target_label)
	bottom = [0] * len(target_label)
	left = [width] * len(target_label)
	right = [0] * len(target_label)
	centroid_x = [0] * len(target_label)
	centroid_y = [0] * len(target_label)
	count = [0] * len(target_label)
	for row in range(height):
		for col in range(width):
			if img_bin[row][col] in target_label:
				n = target_label.index(img_bin[row][col])
				if row < top[n]:
					top[n] = row
				if row > bottom[n]:
					bottom[n] = row
				if col < left[n]:
					left[n] = col
				if col > right[n]:
					right[n] = col
				centroid_x[n] += col
				centroid_y[n] += row
				count[n] += 1
	for i in range(len(target_label)):
		centroid_x[i] = int(centroid_x[i]/count[i])
		centroid_y[i] = int(centroid_y[i]/count[i])


	return left, right, top, bottom, centroid_x, centroid_y

def draw_histogram(img):
	hist_img = [0] * 256
	for row in range(img.shape[0]):
		for col in range(img.shape[1]):
			pix = img[row][col]
			hist_img[pix] += 1
	plt.bar(range(len(hist_img)), hist_img, width = 2)
	return plt


def draw_rectangle(img, left, right, top, bottom, color):
    # Draw top & bottom
    for x in range(left, right + 1):
        img[top][x] = color
        img[bottom][x] = color

    # Draw left & right
    for y in range(top, bottom + 1):
        img[y][left] = color
        img[y][right] = color

def draw_centroid(img, centroid_x, centroid_y, color):
	centroid_size = 12
	for x in range(int(centroid_x - centroid_size/2), int(centroid_x + centroid_size/2)):
		img[x][centroid_y] = color
	for y in range(int(centroid_y - centroid_size/2), int(centroid_y + centroid_size/2)):
		img[centroid_x][y] = color


if __name__ == '__main__':

	FileName = '236_0.81410295.jpg'

	#以灰階讀入圖片; 0代表cv2.IMREAD_GRAYSCALE, 1代表cv2.IMREAD_COLOR, 
	#			  -1代表cv2.IMREAD_UNCHANGED
	img = cv2.imread(FileName, 0)
	
	#2.
	plt = draw_histogram(img)
	plt.savefig(FileName+'_histogram.jpg')
	print(FileName+'_histogram.jpg'+' saved!')

	#1.
	img = convert2BinaryImage(img)
	cv2.imwrite(FileName+'_BinaryImage.jpg', img)
	print(FileName+'_BinaryImage.jpg'+' saved!')

	#3.
	img_bin, bin_list = Connected_Components(img)
	left, right, top, bottom, centroid_x, centroid_y = find_regionPoint(img_bin, bin_list, target_value = 500)

	img1 = cv2.imread(FileName+'_BinaryImage.jpg', 1)
	for i in range(len(left)):
		draw_rectangle(img1, left[i], right[i], top[i], bottom[i], (0, 255, 0))
		draw_centroid(img1, centroid_y[i], centroid_x[i], (0, 255, 0))

	cv2.imwrite(FileName+'_Connected_Components.jpg', img1)
	print(FileName+'_Connected_Components.jpg'+' saved!')
