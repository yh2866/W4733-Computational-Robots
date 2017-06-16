import heapq
import math


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


    def isSame(self, u):
        return self.x == u.x and self.y == u.y


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



if __name__ == "__main__":
    graph = Graph([(0, 0), (1, 1), (1, 2), (2, 1), (2, 2), (3,1), (3, 2)])

    graph.addUndirectedEdge(0, 1)
    graph.addUndirectedEdge(1, 2)
    graph.addUndirectedEdge(1, 3)
    graph.addUndirectedEdge(3, 2)
    graph.addUndirectedEdge(2, 4)
    graph.addUndirectedEdge(2, 5)

    graph.dijkstra(0)
    print(graph.shortestPath(0, 5))


