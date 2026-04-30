import numpy as np
import cv2
import imutils


def mask_image(img):
    mask = np.zeros((img.shape[0],img.shape[1]),dtype = "uint8")
    for i in range(0,4):
        bbox = cv2.selectROI(img,False)
        print(bbox)
        #hit spacebar after creating box
        #after using the fucntion above to get points of our masked area we do the following 

test1 = cv2.imread("ring_test_image.jpg")