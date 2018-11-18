import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

#以灰階讀入圖片; 0代表cv2.IMREAD_GRAYSCALE, 1代表cv2.IMREAD_COLOR, 
#			  -1代表cv2.IMREAD_UNCHANGED

FileName = 'lena.bmp'
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


def draw_rectangle(img, left, right, top, bottom, color):
    # Draw top & bottom
    for x in range(left, right + 1):
        img[top][x] = color
        img[bottom][x] = color

    # Draw left & right
    for y in range(top, bottom + 1):
        img[y][left] = color
        img[y][right] = color





img_bin, bin_list = Connected_Components(img)
bin_count = [0] * len(bin_list)
#print(bin_list)

for row in range(height):
	for col in range(width):
		if img_bin[row][col] != -1:
			bin_count[bin_list.index(img_bin[row][col])] += 1
for n, i in enumerate(bin_count):
	if i > 500:
		print(str(bin_list[n])+' : '+str(bin_count[n]))

top = height
bottom = 0
left = width
right = 0
for row in range(height):
	for col in range(width):
		if img_bin[row][col] == 7554:
			if row < top:
				top = row
			if row > bottom:
				bottom = row
			if col < left:
				left = col
			if col > right:
				right = col

img1 = cv2.imread('BinaryImage_lena.bmp', 1)


draw_rectangle(img1, left, right, top, bottom, (255, 127, 0))
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


