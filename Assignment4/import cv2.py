import cv2
import numpy as np
from matplotlib import pyplot as plt

np.set_printoptions(suppress=True)


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

    print "Please select the color by clicking on the screen..."
    cvimage = cv2.imread(img)
    cv2.imshow('image', cvimage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #obtain the matrix of the selected points
    print "The clicked points..."
    print list_of_clicks
    return list_of_clicks


def get_threshold(hsv):

    h = cv2.calcHist([hsv],[0],None,[180],[0,180])
    h.astype(np.uint8)

    s = cv2.calcHist([hsv],[1],None,[256],[0,256])
    s.astype(np.uint8)

    v = cv2.calcHist([hsv],[2],None,[256],[0,256])
    v.astype(np.uint8)

    # print "h ", np.argmax(h)
    # print "s ", np.argmax(s)
    # print "v ", np.argmax(v)

    plt.plot(h.flatten(), 'r')
    plt.plot(s.flatten(), 'b')
    plt.plot(v.flatten(), 'g')
    plt.show()

    # print "h ", h
    # print "s ", s
    # print "v ", v

    h_min = max(0, np.argmax(h) - 15)
    h_max = min(179, np.argmax(h) + 15)

    s_min = max(0, np.argmax(s) - 15)
    s_max = min(255, np.argmax(s) + 15)

    v_min = max(0, np.argmax(v) - 15)
    v_max = min(255, np.argmax(v) + 15)

    print "h_min ", h_min
    print "h_max ", h_max
    print "s_min ", s_min
    print "s_max ", s_max
    print "v_min ", v_min
    print "v_max ", v_max

    return h_min, h_max, s_min, s_max, v_min, v_max



def mask_hsv_img(hsv, h_min, h_max, s_min, s_max, v_min, v_max):
    mask = cv2.inRange(hsv, np.array([h_min, s_min, v_min], dtype = 'uint8'), np.array([h_max, s_max, v_max], dtype = 'uint8'))
    output = cv2.bitwise_and(hsv, hsv, mask = mask)

    im_hsv = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)
    im_gray = cv2.cvtColor(im_hsv, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    kernel = np.ones((3,3), np.uint8)
    img_erosion = cv2.erode(im_gray, kernel, iterations=1)
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)

    return img_dilation


def get_centroid_area(img):
    img_cpy = np.copy(img)

    contours, hierarchy = cv2.findContours(img_cpy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # maxContourData = 0
    maxArea = 0
    M = 0

    print "contours ", len(contours)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > maxArea:
            maxArea = area
            # maxContourData = contour
            M = cv2.moments(contour)

    cx = M['m10'] / M['m00']
    cy = M['m01'] / M['m00']

    print "cx ", cx, " cy ", cy
    print "area ", maxArea

    return cx, cy, maxArea


if __name__ == "__main__":
    img_str = "img6.jpg"

    list_of_clicks = getXY(img_str)
    frame = cv2.imread(img_str)
    # print "frame ", frame.shape

    print "list_of_clicks x ", list_of_clicks[0][0], " ", list_of_clicks[1][0]
    print "list_of_clicks y ", list_of_clicks[0][1], " ", list_of_clicks[1][1]

    rectangle = []

    for i in range(list_of_clicks[0][0], list_of_clicks[1][0]):
        print "i ", i
        row = []
        for j in range(list_of_clicks[0][1], list_of_clicks[1][1]):
            print "frame i, j", i, " ", j
            row.append(frame[i][j])
        rectangle.append(np.array(row))

    rectangle = np.array(rectangle, dtype = 'uint8')

    print "rec ", rectangle


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv,(5,5),0)

    h_min, h_max, s_min, s_max, v_min, v_max = get_threshold(hsv)



    binary_img = mask_hsv_img(hsv, h_min, h_max, s_min, s_max, v_min, v_max)
    # cx, cy, area = get_centroid_area(binary_img)


    # im_gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # im_gray2 = cv2.GaussianBlur(im_gray2, (5, 5), 0)
    # (thresh, im_bw2) = cv2.threshold(im_gray2, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # detector = cv2.SimpleBlobDetector()
    # keypoints = detector.detect(img_dilation)

    # im_with_keypoints = cv2.drawKeypoints(img_dilation, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # # Show keypoints
    # cv2.imshow("Keypoints", im_with_keypoints)

    # Find the largest contour and extract it

    cv2.imshow("original ", frame)
    cv2.imshow("hsv_binary", binary_img)


    cv2.waitKey()


