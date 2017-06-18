import matplotlib.pyplot as plt
import numpy as np
import heapq
import math


def plot_environment(object):
    plt.plot(object[:,0],object[:,1],'b-')
    plt.plot((object[-1,0],object[0,0]),(object[-1,1],object[0,1]),'b-')
    return

def plot_grown_obstacle(object):
    plt.plot(object[:,0],object[:,1],'r-')
    plt.plot((object[-1,0],object[0,0]),(object[-1,1],object[0,1]),'r-')
    plt.plot(object[:,0],object[:,1],'ko')
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
    # print "rightmost:", points_array[0]

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
    if(result>0):
        return True
    return False

def discard(result):
    if(find_angle(result[1],result[0]) == find_angle(result[0],result[-1])):
        result.remove(result[-1])
    for i in range(1, len(result)-1):
        pre_an = find_angle(result[i-1], result[i])
        cur_an = find_angle(result[i], result[i+1])
        print "result[i]=",result[i]
        print "angle==========",pre_an, cur_an
        if(pre_an == cur_an):
            result.remove(result[i])
    if(find_angle(result[-2],result[-1]) - find_angle(result[-1],result[0]) < 0.0001):
        result.remove(result[-1])
    print "result=====",result
    return result

def graham_scan(points_array):
    points_array = sort_points(points_array)
    # print points_array

    s = [] #push pop size
    s.append(points_array[-1])
    s.append(points_array[0])
    for point in points_array[1:]:
        #print point
        while len(s)>1 and toTheLeft(point, s[-1], s[-2])==False:
            s.pop()
        s.append(point)
    #extract points from stack
    result = []
    for i in range(len(s)):
        result.append(s.pop())
    #discard redundant points on the same line
    #result = discard(result)
    return result



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

            if not self.vertices[vId].visited:
                if backpointer != None :
                    print "cost ", cost, " vId", vId, " loc ", self.vertices[vId].x, ", ", self.vertices[vId].y, " backpointer ", backpointer, " loc ", self.vertices[backpointer].x, ", ", self.vertices[backpointer].y
                self.vertices[vId].visited = True
                self.vertices[vId].cost = cost
                self.vertices[vId].backpointer = backpointer


                for e in self.vertices[vId].adj:
                    if not self.vertices[e.targetVId].visited:
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

def check_intersect(segment1, segment2):
    X1 = segment1[0][0]
    X2 = segment1[1][0]
    Y1 = segment1[0][1]
    Y2 = segment1[1][1]
    X3 = segment2[0][0]
    X4 = segment2[1][0]
    Y3 = segment2[0][1]
    Y4 = segment2[1][1]


    if (max(X1, X2) < min(X3, X4)):
        # print "False -1"
        return False

    if X1 == X2 or X3 == X4:
        # print "x1 == x2 or x3 == x4"
        if X1 == X2 == X3 == X4:
            return True
        elif X1 == X2:
            # print "x1 == x2"
            A2 = (Y3-Y4)/float(X3-X4)
            b2 = Y3-A2*X3

            if X1 <= min(X3, X4) or X1 >= max(X3, X4):
                return False
            elif A2 * X1 + b2 >= min(Y1, Y2) and A2 * X1 + b2 <= max (Y1, Y2):
                return True
            else:
                return False

        elif X3 == X4:
            # print "x3 == x4"
            # print "Y1 - Y2 ", Y1 - Y2
            # print "X1 - X2 ", X1 - X2
            A1 = (Y1-Y2) / float(X1-X2)
            b1 = Y1-A1*X1

            if X3 <= min(X1, X2) or X3 >= max(X1, X2):
                return False
            elif A1 * X3 + b1 >= min(Y3, Y4) and A1 * X3 + b1 <= max (Y3, Y4):
                return True
            else:
                return False


    # got this portion from stackoverflow

    a1 = (Y1-Y2)/(X1-X2)
    a2 = (Y3-Y4)/(X3-X4)
    b1 = -1;
    b2 = -1;
    c1 = Y1 - a1*X1;
    c2 = Y3 - a2*X3;
    #using the sign function from numpy
    f1_1 = np.sign(a1*X3 + b1*Y3 + c1);
    f1_2 = np.sign(a1*X4 + b1*Y4 + c1);
    f2_1 = np.sign(a2*X1 + b2*Y1 + c2);
    f2_2 = np.sign(a2*X2 + b2*Y2 + c2);
    # print "f1_1",f1_1
    # print "f1_2",f1_2
    # print "f2_1",f2_1
    # print "f2_2",f2_2

    if (f1_1 == f1_2) or (f2_1 == f2_2):
        # print "Not intersect"
        return False
    if (f1_1 != f1_2) and (f2_1 != f2_2):
        # print "Intersect"
        return True


def createEachGrownObjectEdgesList(graph, graham_scan_result_pts_grouped_by_object_list):
    ObjectsEdges = []

    count = 0

    for r in graham_scan_result_pts_grouped_by_object_list:
        for i in range(1, len(r)):
            ObjectsEdges.append([r[i], r[i - 1]])
            graph.addUndirectedEdge(count + i, count + i - 1)
            plt.plot([graph.vertices[count + i].x, graph.vertices[count + i - 1].x], [graph.vertices[count + i].y, graph.vertices[count + i - 1].y], 'y-')

        ObjectsEdges.append([r[0], r[-1]])
        graph.addUndirectedEdge(count + len(r) - 1, count)
        plt.plot([graph.vertices[count + len(r) - 1].x, graph.vertices[count].x], [graph.vertices[count + len(r) - 1].y, graph.vertices[count].y], 'y-')
        count += len(r)

    return ObjectsEdges


def connectDiffObjectsWithEdges(graph, graham_scan_result_pts_grouped_by_object_list, ObjectsEdges):

    for i in range(len(graham_scan_result_pts_grouped_by_object_list)):
        for j in range(i + 1, len(graham_scan_result_pts_grouped_by_object_list)):

            r1 = graham_scan_result_pts_grouped_by_object_list[i]
            r2 = graham_scan_result_pts_grouped_by_object_list[j]

            for k in range(len(r1)):
                for l in range(len(r2)):

                    startPt = r1[k]
                    endPt = r2[l]

                    testEdges = []

                    for e in ObjectsEdges:
                        if e[0] != startPt and e[1] != startPt and e[0] != endPt and e[1] != endPt:
                            testEdges.append(e)


                    testPass = True

                    for e in testEdges:
                        if check_intersect([startPt, endPt], e):
                            testPass = False

                    sIdx = 0
                    gIdx = 0

                    if testPass:
                        for idx in range(0, i):
                            sIdx += len(graham_scan_result_pts_grouped_by_object_list[idx])
                        sIdx += k

                        for idx in range(0, j):
                            gIdx += len(graham_scan_result_pts_grouped_by_object_list[idx])
                        gIdx += l

                        # print " startPt ", startPt, " idx ", sIdx
                        # print " endPt ", endPt, " idx ", gIdx
                        # print "testPass ", testPass
                        # print "i ", i, " j ", j

                        graph.addUndirectedEdge(sIdx, gIdx)
                        plt.plot([graph.vertices[sIdx].x, graph.vertices[gIdx].x], [graph.vertices[sIdx].y, graph.vertices[gIdx].y], 'y-')

    return graph


def generateGraphPts(graham_scan_result_pts_grouped_by_object_list):
    pts = []

    for r in graham_scan_result_pts_grouped_by_object_list:
        pts += r

    return pts


def parseData(filename):
    with open(filename) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    print(content)

    startx, starty = map(float, content[0].split())
    start_point = [startx, starty]

    goalx, goaly = map(float, content[1].split())
    goal_point = [goalx, goaly]

    dimensions_x, dimensions_y = map(float, content[2].split())

    numObj = int(content[3])

    contentIdx = 4
    objects = []

    for i in range(numObj):
        object = []

        vertices = int(content[contentIdx])
        contentIdx += 1

        for j in range(vertices):
            x, y = map(float, content[contentIdx].split())
            object.append([x, y])
            contentIdx += 1

        objects.append(object)

    print "objects ", objects
    print "\n"

    return start_point, goal_point, objects, dimensions_x, dimensions_y


def graphData(start_point, goal_point, objects):
    plt.plot(start_point[0],start_point[1],'go',ms=10)
    plt.plot(goal_point[0],goal_point[1],'go',ms=10)

    for object in objects:
        plot_environment(np.array(object))


def growAndGrahamScanObjects(objects, start_point, goal_point):
    grown_object_pts_list = []

    for object in objects:
        grown_object_pts_list.append([list(x) for x in grown_obstacle(object)])

    graham_scan_result_pts_grouped_by_object_list = []

    for pts in grown_object_pts_list:
        r = graham_scan(pts)
        plot_grown_obstacle(np.array(r))
        graham_scan_result_pts_grouped_by_object_list.append(r)

    graham_scan_result_pts_grouped_by_object_list.append([start_point])
    graham_scan_result_pts_grouped_by_object_list.append([goal_point])

    return graham_scan_result_pts_grouped_by_object_list


def getOptimalPathPts(graph):
    graph.dijkstra(len(graph.vertices) - 2)
    result_vertex_indices = graph.shortestPath(len(graph.vertices) - 2, len(graph.vertices) - 1)

    result = []

    for i in result_vertex_indices:
        result.append([graph.vertices[i].x, graph.vertices[i].y])

    print(result)

    return result


def plotOptimalPath(result):
    # plot shortest path
    for i in range(1, len(result)):
        plt.plot([result[i - 1][0], result[i][0]], [result[i - 1][1], result[i][1]], 'g-')



def pathPlanning():
    start_point, goal_point, objects, dimensions_x, dimensions_y = parseData("test1.txt")
    graphData(start_point, goal_point, objects)

    graham_scan_result_pts_grouped_by_object_list = growAndGrahamScanObjects(objects, start_point, goal_point)

    pts = generateGraphPts(graham_scan_result_pts_grouped_by_object_list)
    graph = Graph(pts)

    ObjectsEdges = createEachGrownObjectEdgesList(graph, graham_scan_result_pts_grouped_by_object_list)
    graph = connectDiffObjectsWithEdges(graph, graham_scan_result_pts_grouped_by_object_list, ObjectsEdges)

    result = getOptimalPathPts(graph)
    plotOptimalPath(result)


    plt.xlim([0,dimensions_x])
    plt.ylim([0,dimensions_y])
    plt.show()



if __name__ == "__main__":
    pathPlanning()





