import cv2
import numpy as np


cv2.namedWindow('image')
frame = cv2.imread('orange.jpg')


hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# print "frame ", frame

cv2.imshow("image", frame)
cv2.waitKey()

x, y, z = hsv.shape
a = np.reshape(hsv, (x * y, z))

print "x ", x, " y", y, " z", z


thresh = np.mean(a, axis = 0)

print "thresh ", thresh
result = []

print "size ", np.size(a)



for t in a:
    # print "t ", t
    if t[0] > thresh[0] and t[1] > thresh[1] and t[2] > thresh[2]:
        # print "yes"
        result.append(np.array([0, 0, 0]))
    else:
        # print "no"
        result.append(np.array([0, 0, 0]))

# result = np.reshape(np.array(result), (x, y, z))
# a, b, c = result.shape

# print "a ", a, " b", b, " c", c
# for t in result:
#     print "t ", t



np.savetxt("file.txt", np.array(result), fmt = '%i')

cv2.imshow("image", np.reshape(np.array(result), (x, y, z)))
cv2.waitKey()

