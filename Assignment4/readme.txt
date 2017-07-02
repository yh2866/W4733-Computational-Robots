# How to run the program

1. Run python2 main.py. This will capture a picture and show the image on the screen.

2. Click two points (upper left, lower right - which translates to a rectangle) on the image (target object)

3. Click Enter. A window that contains the binary image of the target object will show up.

4. Click Enter. Gopigo will now start to track the target object.



# How we compute the trehshold to segment the target object

We convert bgr format image to hsv. Then we create a histogram for h, s and v. For each of h, s and v, we find the value with the highest frequency. The upper and lower limits become +- 20 from the highest frequency value.

# Note that our image segmentation works best with a target object that has a unique uniform color (as specified in the assignment instruction)