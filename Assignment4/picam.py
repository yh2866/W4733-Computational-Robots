import picamera
import cv2
import numpy as np
import time

#create an instance of PiCamera
camera = picamera.PiCamera()

#iterates through the loop 10 times
k = 0 
while(True and k < 2):

    #saves what the robot currently sees 
    camera.capture('img_org' + str(k) + '.jpg')
    img = cv2.imread('img_org' + str(k) + '.jpg')

	#apply mask with lower and upper blue H values
    lower_blue = np.array([60,50,50])
    upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(img, lower_blue, upper_blue)

    #save image with number
    cv2.imwrite('img'+str(k)+'.jpg',mask)
    
    k = k + 1
    time.sleep(10)

