import cv2
import numpy as np
from matplotlib import pyplot as plt

np.set_printoptions(suppress=True)

frame = cv2.imread('img.jpg')

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
hsv = cv2.GaussianBlur(hsv,(5,5),0)

h = cv2.calcHist([hsv],[0],None,[180],[0,180])
h.astype(np.uint8)


s = cv2.calcHist([hsv],[1],None,[255],[0,255])
s.astype(np.uint8)


v = cv2.calcHist([hsv],[2],None,[255],[0,255])
v.astype(np.uint8)



print "h ", np.argmax(h)
print "s ", np.argmax(s)
print "v ", np.argmax(v)

plt.plot(h.flatten(), 'r')
plt.plot(s.flatten(), 'b')
plt.plot(v.flatten(), 'g')
plt.show()

# print "h ", h
# print "s ", s
# print "v ", v

h_min = max(0, np.argmax(h) - 10)
h_max = min(179, np.argmax(h) + 10)

s_min = max(0, np.argmax(s) - 10)
s_max = min(255, np.argmax(s) + 10)

v_min = max(0, np.argmax(v) - 10)
v_max = min(255, np.argmax(v) + 10)

mask = cv2.inRange(hsv, np.array([h_min, 50, 50]), np.array([h_max, 255, 255]))
output = cv2.bitwise_and(hsv, hsv, mask = mask)

im_hsv = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)
im_gray = cv2.cvtColor(im_hsv, cv2.COLOR_BGR2GRAY)
im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)
(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)



im_gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
im_gray2 = cv2.GaussianBlur(im_gray2, (5, 5), 0)
(thresh, im_bw2) = cv2.threshold(im_gray2, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)


cv2.imshow("original ", frame)
cv2.imshow("hsv_binary", im_bw)
cv2.imshow("otsu+binary", im_bw2)

cv2.waitKey()


# print "x ", x, " y", y, " z", z


# thresh = np.mean(a, axis = 0)

# print "thresh ", thresh
# result = []

# print "size ", np.size(a)



# for t in a:
#     # print "t ", t
#     if t[0] > thresh[0] and t[1] < thresh[1] and t[2] < thresh[2]:
#         # print "yes"
#         result.append(np.array([255, 255, 255], dtype=np.uint8))
#     else:
#         # print "no"
#         result.append(np.array([0, 0, 0], dtype=np.uint8))

# # result = np.reshape(np.array(result), (x, y, z))
# # a, b, c = result.shape

# # print "a ", a, " b", b, " c", c
# # for t in result:
# #     print "t ", t



# np.savetxt("file.txt", np.array(result), fmt = '%i')
# result = np.reshape(np.array(result), (x, y, z))

# blur = cv2.GaussianBlur(result,(5,5),0)
# kernel = np.ones((5,5), np.uint8)
# img_erosion = cv2.erode(blur, kernel, iterations=20)
# img_dilation = cv2.dilate(img_erosion, kernel, iterations=20)

# cv2.imshow("image", result)
# cv2.waitKey()

# img = cv2.imread('image.jpg',0)

# # Find the largest contour and extract it
# ret, Ithres = cv2.threshold(Rfilter,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# im, contours, hierarchy = cv2.findContours(Ithres,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE )

# maxContour = 0
# for contour in contours:
#     contourSize = cv2.contourArea(contour)
#     if contourSize > maxContour:
#         maxContour = contourSize
#         maxContourData = contour

# # Create a mask from the largest contour
# mask = np.zeros_like(Ithres)
# cv2.fillPoly(mask,[maxContourData],1)

# # Use mask to crop data from original image
# finalImage = np.zeros_like(Irgb)
# finalImage[:,:,0] = np.multiply(R,mask)
# finalImage[:,:,1] = np.multiply(G,mask)
# finalImage[:,:,2] = np.multiply(B,mask)
# cv2.imshow('final',finalImage)
# cv2.waitKey()
