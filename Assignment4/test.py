import cv2
import numpy as np

def nothing():
    print "nothing"

cv2.namedWindow('image')
frame = cv2.imread('orange.jpg')
hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

np.mean(hsv[:][, axis =)

print "hsv", hsv

cv2.waitKey(0)
cv2.destroyAllWindows()