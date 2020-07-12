"""
图的邻接表表示法
A->B
B->C->D
C
D->A
"""
from typing import List
from queue import Queue

INFINITY = 65535


class Edge:
    def __init__(self, v1: int, v2: int, weight: int):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight


class Node:
    def __init__(self, v: int, weight: int):
        """
        节点
        :param v: 节点下标
        :param weight: 边权重
        """
        self.v = v
        self.weight = weight
        self.next = None


class Graph:
    def __init__(self):
        self.nv = 0
        self.ne = 0
        self.graph = []
        self.visited = []

    def insert_edge(self, edge: List[int]):
        new_node = Node(edge[1], edge[2])
        new_node.next = self.graph[edge[0]]

        self.graph[edge[0]] = new_node

    def create_graph(self, nv: int, ne: int, edges: List[List[int]]):
        self.nv = nv
        self.ne = ne

        for _ in range(ne):
            self.graph.append(None)
            self.visited.append(False)

        for edge in edges:
            self.insert_edge(edge)

    def visit(self, v):
        print('Visit Node {}'.format(v))
        self.visited[v] = True

    def init_visit(self):
        for v in range(self.nv):
            self.visited[v] = False

    # 1. 广度优先遍历
    def broad_first_search(self, v: int):
        q = Queue()
        self.visit(v)
        q.put(v)

        while not q.empty():
            v = q.get()
            w = self.graph[v]

            while w:
                if not self.visited[w]:
                    self.visit(w.v)
                    q.put(w.v)
                w = w.next

    # 2. 深度有限遍历
    def deep_first_search(self, v: int):
        self.visit(v)

        w = self.graph[v]
        while w:
            if not self.visited[w.v]:
                self.deep_first_search(w.v)
            w = w.next

    # 3.  无权图的单源最短路径算法
    def unweighted(self, dist: List[int], path: List[int], s: int):
        q = Queue()

        for _ in range(self.nv):
            dist.append(-1)
            path.append(-1)

        dist[s] = 0
        q.put(s)

        while not q.empty():
            v = q.get()
            w = self.graph[v]
            while w:
                if dist[w.v] == -1:
                    # 没有被访问过
                    dist[w.v] = dist[v] + 1
                    path[w.v] = v
                    q.put(w.v)
                w = w.next

    # 4. 有权图的单源最短路径算法
    def find_min_dist(self, dist: List[int], collected: List[int]):
        min_v = 0
        min_dist = INFINITY

        for v in range(self.nv):
            if not collected[v] and dist[v] < min_dist:
                min_dist = dist[v]
                min_v = v
        if min_dist < INFINITY:
            return min_v
        else:
            return None

    def dijkstra(self, dist, path, s):
        collected = []
        for v in range(self.nv):
            collected.append(False)
            dist.append(INFINITY)
            path.append(-1)

        dist[s] = 0

        while True:
            v = self.find_min_dist(dist, collected)
            if v is None:
                break
            collected[v] = True

            w = self.graph[v]
            while w:
                if not collected[w.v] and dist[w.v] > dist[v] + w.weight:
                    dist[w.v] = dist[v] + w.weight
                    path[w.v] = v
                w = w.next


if __name__ == '__main__':
    edges = [
        [1, 0, 1],
        [1, 3, 2],
        [1, 2, 3],
        [2, 4, 4],
        [3, 4, 4],
    ]

    g = Graph()
    g.create_graph(5, 5, edges)
    dist = []
    path = []
    g.dijkstra(dist, path, 1)
    print(dist, path)

    edges = [
        [0, 1, 2],
        [0, 3, 1],
        [1, 3, 3],
        [1, 4, 10],
        [2, 0, 4],
        [2, 5, 5],
        [3, 4, 2],
        [3, 5, 8],
        [3, 6, 4],
        [3, 2, 2],
        [4, 6, 6],
        [6, 5, 1]
    ]
    g.create_graph(7, 12, edges)
    dist, path = [], []
    g.unweighted(dist, path, 2)
    print(dist, path)
    dist = []
    path = []
    g.dijkstra(dist, path, 0)
    print(dist, path)

