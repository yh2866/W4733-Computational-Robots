#The video link can be found at here:
https://youtu.be/2wnC_YX2c5A

# How to run the program
1. Run python2 main.py. This will capture a picture and show the image on the screen.
2. Click two points (upper left, lower right - which translates to a rectangle) on the image (target object)
3. Click Enter. A window that contains the binary image of the target object will show up.
4. Click Enter. Gopigo will now start to track the target object.

# How we compute the threshold to segment the target object
We convert RGB format image to HSV. Then we create a histogram for h, s and v. For each of h, s and v, we find the value with the highest frequency. The upper and lower limits become +- 20 from the highest frequency value. Note that our image segmentation works best with a target object that has a unique uniform color (as specified in the assignment instruction) Based on the segment we got, we use the erosion and dilation to improve the segment. And then we use the ¡®findcontours¡¯ and ¡®contourarea¡¯ functions to get the centroid and area of the segment.

#How we let the robot move
The main.py will use the move.py which include the move functions. For the move function, it saves the first area and compares the later area with the initial value, if the area is 10% bigger than the initial value it will move backward, if the area is 10% smaller than the initial value it will move forward. For the rotation, it is decided by the x value of centroid, if the x value is smaller than the middle of width, it will turn left, if the x value is bigger than the middle of width, it will turn right.

#If there is any problem, feel free to contact us by email: yh2866@columbia.edu