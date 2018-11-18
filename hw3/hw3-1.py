import cv2
from matplotlib import pyplot as plt
def histogram_equalization(img):
	size = img.shape[0] * img.shape[1]
	sum = 0

	hist_img = histogram(img)
	for i in range(len(hist_img)):
		sum += hist_img[i]/size
		hist_img[i] = int(255 * sum)

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
	hist_img = histogram(img)
	plt.bar(range(len(hist_img)), hist_img, width = 1)
	plt.savefig(FileName+'_histogram.jpg')

	plt.clf()	#clear current figure in plot
	img_HisEq = histogram_equalization(img)
	
	#cv2.imshow(img)
	cv2.imwrite(FileName+'_HistogramEquli.bmp', img_HisEq)
	
	hist_img_HisEq = histogram(img_HisEq)
	plt.bar(range(len(hist_img_HisEq)), hist_img_HisEq, width = 1)	
	plt.savefig(FileName+'_HisEq_histogram.jpg')






