import matplotlib.pyplot as plt
import numpy as np
import heapq
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

def plot_grown_obstacle(object):
    plt.plot(object[:,0],object[:,1],'r-')
    plt.plot((object[-1,0],object[0,0]),(object[-1,1],object[0,1]),'r-')
    plt.plot(object[:,0],object[:,1],'ko')
    return

def plot_shortestPath(object):
    plt.plot(object[:,0],object[:,1],'g-')
    plt.plot((object[-1,0],object[0,0]),(object[-1,1],object[0,1]),'g-')
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
        #plt.plot(grown_obstacle[:,0],grown_obstacle[:,1],'ko')
    return grown_obstacle



# # Function to know if we have a CCW turn
# def RightTurn(p1, p2, p3):
#     if (p3[1]-p1[1])*(p2[0]-p1[0]) >= (p2[1]-p1[1])*(p3[0]-p1[0]):
#         return False
#     return True
    
# # Main algorithm:
# def GrahamScan(P):
#     P.sort()            # Sort the set of points
#     L_upper = [P[0], P[1]]      # Initialize upper part
#     # Compute the upper part of the hull
#     for i in range(2,len(P)):
#         L_upper.append(P[i])
#         while len(L_upper) > 2 and not RightTurn(L_upper[-1],L_upper[-2],L_upper[-3]):
#             del L_upper[-2]
#     L_lower = [P[-1], P[-2]]    # Initialize the lower part
#     # Compute the lower part of the hull
#     for i in range(len(P)-3,-1,-1):
#         L_lower.append(P[i])
#         while len(L_lower) > 2 and not RightTurn(L_lower[-1],L_lower[-2],L_lower[-3]):
#             del L_lower[-2]
#     del L_lower[0]
#     del L_lower[-1]
#     L = L_upper + L_lower       # Build the full hull
#     return np.array(L)


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
        if(points_array[i][1]==up):
            if(rightmost[0]<points_array[i][0]):
                rightmost = points_array[i]
        if(points_array[i][1]<up):  #below the curr
            #if(rightmost[0]<points_array[i][0]):   #to the right of curr
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
        while len(s)>1 and toTheLeft(point, s[-1], s[-2])==False:
            s.pop()
        s.append(point)
        """
        if(toTheLeft(point, s[-1], s[-2])):
            s.append(point)
            print s,point
        else:
            s.pop()
            print s,point
        """
    #extract points from stack
    result = []
    for i in range(len(s)):
        result.append(s.pop())
    if(result[-1]==result[0]):
        result = result[0:-1]
    return result[::-1] #reverse list



class Edge:
    def __init__(self, targetVId, cost):
        self.targetVId = targetVId
        self.cost = cost


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = float('inf')
        self.adj = []
        self.visited = False
        self.backpointer = None


class Graph:
    def __init__(self, pairs):
        self.vertices = []

        for p in pairs:
            self.vertices.append(Vertex(p[0], p[1]))


    def addEdge(self, uId, vId):
        cost = self.computeEuclidean(uId, vId)
        e = Edge(vId, cost)
        self.vertices[uId].adj.append(e)


    def addUndirectedEdge(self, uId, vId):
        self.addEdge(uId, vId)
        self.addEdge(vId, uId)


    def computeEuclidean(self, uId, vId):
        return math.sqrt(math.pow(self.vertices[uId].x - self.vertices[vId].x, 2) +
            math.pow(self.vertices[uId].y - self.vertices[vId].y, 2))


    # s is the start vertex Id
    def dijkstra(self, sId):
        pq =[]

        heapq.heappush(pq, (0, sId, None))

        while pq:
            cost, vId, backpointer = heapq.heappop(pq)
            print("v x ", self.vertices[vId].x)
            print("v y ", self.vertices[vId].y)
            if not self.vertices[vId].visited:
                self.vertices[vId].visted = True
                self.vertices[vId].cost = cost
                self.vertices[vId].backpointer = backpointer

                for e in self.vertices[vId].adj:

                    if self.vertices[vId].cost + e.cost < self.vertices[e.targetVId].cost:
                        cost = self.vertices[vId].cost + e.cost
                        heapq.heappush(pq, (cost, e.targetVId, vId))




    def shortestPath(self, sId, gId):
        self.dijkstra(sId)
        stk = []

        vId = gId

        while(vId != sId):
            stk.append(vId)
            vId = self.vertices[vId].backpointer
        stk.append(sId)

        result = []

        while stk:
            result.append(stk.pop())

        return result


def detect_intersect(segment1, segment2):
    x1 = segment1[0][0]
    x2 = segment1[1][0]
    y1 = segment1[0][1]
    y2 = segment1[1][1]
    x3 = segment2[0][0]
    x4 = segment2[1][0]
    y3 = segment2[0][1]
    y4 = segment2[1][1]
    if x1!=x2 and x3!=x4: 
        a1 = (y1-y2)/(x1-x2)
        a2 = (y3-y4)/(x3-x4)
    elif x1==x2:
        a1 = 10000;
    elif x3==x4:
        a2 = 10000;
    b1 = -1;
    b2 = -1;
    c1 = y1 - a1*x1;
    c2 = y3 - a2*x3;
    #using the sign function from numpy
    f1_1 = np.sign(a1*x3 + b1*y3 + c1);
    f1_2 = np.sign(a1*x4 + b1*y4 + c1);
    f2_1 = np.sign(a2*x1 + b2*y1 + c2);
    f2_2 = np.sign(a2*x2 + b2*y2 + c2);
    print "f1_1",f1_1
    print "f1_2",f1_2
    print "f2_1",f2_1
    print "f2_2",f2_2

    if (f1_1 == f1_2) or (f2_1 == f2_2):
        print "Not intersect"
        return False
    if (f1_1 != f1_2) and (f2_1 != f2_2):
        print "Intersect"
        return True


if __name__ == "__main__":
    plt.plot(start_point[0],start_point[1],'go',ms=10)
    plt.plot(goal_point[0],goal_point[1],'go',ms=10)
    plot_environment(object1)
    plot_environment(object2)
    plot_environment(object3)
    plot_environment(object4)

    a = [list(x) for x in grown_obstacle(object1)]
    b = [list(x) for x in grown_obstacle(object2)]
    c = [list(x) for x in grown_obstacle(object3)]
    d = [list(x) for x in grown_obstacle(object4)]

    r1 = graham_scan(a)
    r2 = graham_scan(b)
    r3 = graham_scan(c)
    r4 = graham_scan(d)

    plot_grown_obstacle(np.array(r1))
    plot_grown_obstacle(np.array(r2))
    plot_grown_obstacle(np.array(r3))
    plot_grown_obstacle(np.array(r4))

    # r = a + b + c + d

    # graph = Graph(r)

    # for i in range(len(r)):
    #     for j in range(i + 1, len(r)):
    #         graph.addUndirectedEdge(i, j)

    # r.append(start_point)
    # r.append(goal_point)

    # graph.dijkstra(len(r) - 2)
    # result_vertex_indices = graph.shortestPath(len(r) - 2, len(r) - 1)

    # result = []

    # for i in result_vertex_indices:
    #     result.append([graph.vertices[i].x, graph.vertices[i].y])

    # print(result)

    # plot_shortestPath(np.array(result))

    plt.xlim([0,dimensions_x])
    plt.ylim([0,dimensions_y])
    plt.show()





