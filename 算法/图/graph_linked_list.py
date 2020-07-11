"""
图的邻接表表示法
A->B
B->C->D
C
D->A
"""
from typing import List
from queue import Queue


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
    
