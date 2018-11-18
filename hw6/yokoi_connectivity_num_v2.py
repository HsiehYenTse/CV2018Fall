import cv2
import numpy as np 

def Convert2BinaryImage(img, threshold, mode=0):
    height = img.shape[0]
    width = img.shape[1]
    #convert grayscale into binary image, threshold is 128
    value = 255
    if mode == 1:
        value = 1
    for row in range(height):
        for col in range(width):
            pix = img[row][col]
            if pix >= threshold:
                img[row][col] = value
            else:
                img[row][col] = 0
    return img

def DownSampling(img, size):
    (height, width) = size
    ratio_x = int(img.shape[1] / width)
    ratio_y = int(img.shape[0] / height)
    result = np.ones((height, width))
    for row in range(height):
        for col in range(width):
            result[row][col] = img[row*ratio_y][col*ratio_x]
    return result

def H(b, c, d, e):
    if b == c and (d != b or e != b):
        return 'q'
    if b == c and d == b and e == b:
        return 'r'
    if b != c:
        return 's' 


def YokoiConnNum(img):
    height, width = img.shape
    ans = np.zeros((height, width))
    print(height, width)
    for row in range(height):
        for col in range(width):
            ans[row][col] = -1
            if img[row][col] == 0:
                continue
            neighbors = [0] * 9
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if row+i >= 0 and row+i < height and col+j >= 0 and col+j < width:
                        if img[row+i][col+j] != 0:
                            neighbors[(i+1)*3+j+1] = 1
            a1 = H(neighbors[4], neighbors[5], neighbors[2], neighbors[1])
            a2 = H(neighbors[4], neighbors[1], neighbors[0], neighbors[3])
            a3 = H(neighbors[4], neighbors[3], neighbors[6], neighbors[7])
            a4 = H(neighbors[4], neighbors[7], neighbors[8], neighbors[5])
            A = [a1, a2, a3, a4]
            nq = A.count('q')
            nr = A.count('r')
            if nr == 4:
                ans[row][col] = 5
            else:
                ans[row][col] = nq

    return ans


if __name__ == '__main__':

    filename = 'lena.bmp'
    img = cv2.imread(filename, 0)
    img = Convert2BinaryImage(img, 128)
    small_img = DownSampling(img, (64, 64))
    #cv2.imwrite('img.bmp', small_img)
    ans = YokoiConnNum(small_img)

    f = open('yokoi.txt', 'w')
    for line in ans:
        for ch in line:
            if ch == -1:
                f.write(' ')
            else:
                f.write(str(ch))
        f.write('\n')
    f.close() 









    
