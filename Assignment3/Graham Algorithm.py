import numpy as np
import math

def find_angle(x, y):
    """
    return angle between two points
    """
    return math.atan2(y[1]-x[1], y[0]-x[0])

def sort_points(points_array):
    #find leftmost point
    up = 300
    rightmost = points_array[0]
    for i in range(len(points_array)):
        if(points_array[i][1]<up):  #below the curr
            if(rightmost[0]<points_array[0]):   #to the right of curr
                rightmost = points_array[i]
                up = rightmost[1]
    print "rightmost:", points_array[0]

    #store point with angle
    angle = []
    points = []
    for i in range(0,len(points_array)):
        point = points_array[i]     #extract each point
        points.append(point)
        angle.append(find_angle(rightmost, point))    #find slope

    #sort by angle, result = sorted points CCW
    yx = zip(angle, points)
    yx.sort()
    points = [x for y,x in yx]
    #print points

    return points

#def toTheLeft(point, s1, s2):
def toTheLeft(a, b, c):
    #s2 is the base
    """test cross-product"""
    
    result = (b[1] - a[1]) *(c[0] - a[0]) - (b[0] - a[0]) * (c[1] - a[1])
    if(result>=0):
        return True
    return False
    """
    print s1,s2
    v1 = [(s1[0]-s2[0]),(s1[1]-s2[1])]
    v2 = [(point[0]-s1[0]),(point[1]-s1[1])]
    print "v1v2", v1,v2
    if(np.dot(v1,v2)>=0):
        return True
    else:
        return False
    """

def graham_scan(points_array):
    points_array = sort_points(points_array)
    print points_array

    s = [] #push pop size
    s.append(points_array[-1])
    s.append(points_array[0])
    #print s
    #print "tttte",points_array[1:-1]
    for point in points_array[1:]:
        #print point
        if(toTheLeft(point, s[-1], s[-2])):
            s.append(point)
            print s,point
        else:
            s.pop()
            print s,point

    #extract points from stack
    result = []
    for i in range(len(s)):
        result.append(s.pop())
    if(result[-1]==result[0]):
        result = result[0:-1]
    return result[::-1] #reverse list


points_array = [[1,0],[1,1],[0.5,0],[0,1],[0.5,0.5]]
result = graham_scan(points_array)
print result
