import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


FileName = 'lena.bmp'
#以灰階讀入圖片; 0代表cv2.IMREAD_GRAYSCALE, 1代表cv2.IMREAD_COLOR, 
#			  -1代表cv2.IMREAD_UNCHANGED
img = cv2.imread(FileName, 0)
#print(img.shape)
hist_img = [0] *256
#print(hist_img)

height = img.shape[0]
width = img.shape[1]
#convert grayscale into binary image, threshold is 128
for row in range(height):
	for col in range(width):
		pix = img[row][col]
		hist_img[pix] += 1
		if pix >= 128:
			img[row][col] = 255
		else:
			img[row][col] = 0
#cv2.imwrite('thresh.jpg', img)
def Connected_Components(img):
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
			print(str(bin_list[n])+' : '+str(bin_count[n]))


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





img_bin, bin_list = Connected_Components(img)
left, right, top, bottom, centroid_x, centroid_y = find_regionPoint(img_bin, bin_list, target_value = 500)

img1 = cv2.imread('BinaryImage_lena.bmp', 1)
for i in range(len(left)):
	draw_rectangle(img1, left[i], right[i], top[i], bottom[i], (0, 255, 0))
	draw_centroid(img1, centroid_y[i], centroid_x[i], (0, 255, 0))


#img_bin = np.array(img_bin)

#img1.save('result.bmp')
cv2.imwrite('out.jpg', img1)
'''
f = open('img_bin.txt', 'w')

for row in range(height):
	for col in range(width):
		f.write(str(img_bin[row][col])+' ')
	f.write('\n')
'''


