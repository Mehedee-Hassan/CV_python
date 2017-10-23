
import cv2
import numpy as np

img = cv2.imread('input2.jpg')

row ,cols = img.shape[:2]

kernel_x = cv2.getGaussianKernel(cols,200)
kernel_y = cv2.getGaussianKernel(rows,200)


kernel = kernel_y * kernel_x.T

mask = 255 * kernel / np.linalg.norm(kernel)


output = np.copy(img)


for i in range(3):
    output[:,:,i] = output[:,:,i] * mask

cv2.imshow('original' ,img)
cv2.imshow('vignette' ,output)


cv2.waitkey(0)



# commit :OCV_PyEx: ch2,vignette filter