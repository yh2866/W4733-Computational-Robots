########reading in video + hsv########

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while (1):
     # Take each frame
     _, frame = cap.read()
    # Convert BGR to HSV
   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
-----------------------------------------------

#print out the HSV values for color green
   green = np.uint8([[[0,255,0 ]]])
    hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
    print  hsv_green
    [[[ 60 255 255]]]

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



#####Using mouse to designate region on screen#####

import cv2
import numpy as np
 
list_of_clicks = []
def getXY(img):

   #define the event
   def getxy_callback(event, x, y, flags, param):
    global list_of_clicks
    if event == cv2.EVENT_LBUTTONDOWN :
       list_of_clicks.append([x,y])
       print "click point is...", (x,y)

   #Read the image
   print "Reading the image..."

   #Set mouse CallBack event
   cv2.namedWindow('image')
   cv2.setMouseCallback('image', getxy_callback)


#########finding target (pseudocode)##########

           def get_target(hsv_image):

           #get pixels within threshold of target patch 
	masked_image = mask_image(hsv_image, h_thresh, s_thresh, v_thresh)

	#morphologically erode and dilate the image
                      eroded_image = erosion_filter(masked_image)
	cleaned_image = dilate_filter(erodeed_image)

	#find the largest connected component (largest blob)
	big_blob = get_largest_blob(cleaned_image)

# Compute centroid and area of big_blob to move the robot forward, back, left,, right
         
         centroid = get_centroid(big_blob)
         area = get_area(big_blob)

return centroid, area
