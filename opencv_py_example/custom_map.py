import cv2
import numpy as np 

import math



img= cv2.imread('input.jpg' ,cv2.IMREAD_GRAYSCALE)
rows ,cols = img.shape #height, width, channels = img.shape

img_out = np.zeros(img.shape , dtype=img.dtype)

for i in range(rows):
    for j in range(cols):

        offset_x = int(25.0 * math.cos(2*3.14*i /180))
        offset_y = 0

        if j + offset_x < rows:

            img_out[i ,j] =img[i , (j+offset_x) %cols]
        else :
            img_out[i ,j] = 0


cv2.imshow('Input', img) 
cv2.imshow('Output', img_out) 


cv2.waitKey()







