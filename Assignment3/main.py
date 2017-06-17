import matplotlib.pyplot as plt
import numpy as np
import math

start_point = [10,20]
goal_point = [250,250]
dimensions_x = 300
dimensions_y = 300

object1 = np.array([[200, 220],
                    [221.213203436, 241.213203436],
                    [210.606601718, 251.819805153],
                    [189.393398282, 230.606601718]])

object2 = np.array([[130, 180],
                    [159.997181494, 179.588779362],
                    [145.35287801, 194.640170509]])

object3 = np.array([[150, 120],
                    [194.995772241, 119.383169043],
                    [173.029317014, 141.960255763]])

object4 = np.array([[230, 170],
                    [251.501987353, 190.920433549],
                    [230.503960307, 191.208287996]])


def plot_environment(object):
    plt.plot(object[:,0],object[:,1],'b-')
    plt.plot((object[-1,0],object[0,0]),(object[-1,1],object[0,1]),'b-')
    return

def grown_obstacle(object):
    l = len(object)
    grown_obstacle = np.zeros((4*l,2))
    for i in xrange(l):
        grown_obstacle[0*l+i][0] = object[i][0]
        grown_obstacle[0*l+i][1] = object[i][1]
        grown_obstacle[1*l+i][0] = object[i][0]-23
        grown_obstacle[1*l+i][1] = object[i][1]-23
        grown_obstacle[2*l+i][0] = object[i][0]-23
        grown_obstacle[2*l+i][1] = object[i][1]
        grown_obstacle[3*l+i][0] = object[i][0]
        grown_obstacle[3*l+i][1] = object[i][1]-23
        plt.plot(grown_obstacle[:,0],grown_obstacle[:,1],'ro')
    return grown_obstacle

def find_angle(x, y):
    """
    return angle between two points
    """
    return math.atan2(y[1]-x[1], y[0]-x[0])

def sort_points(points_array):
    #find rightmost point
    up = 300
    rightmost = points_array[0]
    for i in range(len(points_array)):
        if(points_array[i][1]<up):  #below the curr
            if(rightmost[0]<points_array[i][0]):   #to the right of curr
                rightmost = points_array[i]
                up = rightmost[1]
    print "rightmost:", rightmost

    #store point with angle
    angle = []
    points = []
    for i in range(0,len(points_array)):
        point = points_array[i]     #extract each point
        points.append(point)
        angle.append(find_angle(rightmost, point))    #find slope

    #sort by angle, result = sorted points CCW
    yx = zip(angle, points)
    print "yx ", yx
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


if __name__ == "__main__":
    plt.plot(start_point[0],start_point[1],'ro')
    plt.plot(goal_point[0],goal_point[1],'ro')
    plot_environment(object1)
    plot_environment(object2)
    plot_environment(object3)
    plot_environment(object4)
    l = [list(x) for x in grown_obstacle(object1)]
    print "l ", l

    plot_environment(np.array(graham_scan(l)))
    plt.xlim([0,dimensions_x])
    plt.ylim([0,dimensions_y])
    plt.show()





