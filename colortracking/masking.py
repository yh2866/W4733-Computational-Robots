import cv2
import numpy as np




img = cv2.imread('hockney.jpg')
cv2.imshow('Color Image', img)
cv2.waitKey(10000)

mask = cv2.imread('mask.png')
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
thresh = 150
mask = cv2.threshold(mask, thresh, 255, cv2.THRESH_BINARY)[1]
cv2.imshow('Mask Image', mask)
cv2.waitKey(10000)

res = cv2.bitwise_and(img,img, mask=mask)
cv2.imshow('Result', res)
cv2.waitKey(10000)


mask2 = cv2.bitwise_not(mask)
cv2.imshow('Mask 2', mask2)
cv2.waitKey(10000)

res2 = cv2.bitwise_and(img,img, mask=mask2)
cv2.imshow('Result 2', res2)
cv2.waitKey(10000)