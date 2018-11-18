import cv2
import numpy as np 


def DownSampling(img, size):
    height, width = size
    ratio_x = img.shape[1] / width
    ratio_y = img.shape[0] / height
    results = np.zeros((height, width))
    for row in range(height):
        for col in range(width):
            results[row][col] = int(img[int(row*ratio_y)][int(col*ratio_x)])
            print(results[row][col])
    return results

if __name__ == '__main__':

    filename = 'lena.bmp'
    img = cv2.imread(filename, 0)
    result = DownSampling(img, (56, 56))
    print(img)
    cv2.imshow('img', result)
    cv2.waitKey(0)
    
