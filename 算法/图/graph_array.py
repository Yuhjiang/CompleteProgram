"""
邻接矩阵表示法
    A  B  C  D
 A  0  1  0  1
 B  1  0  0  1
 C  0  1  0  1
 D  0  1  1  0
"""
from queue import Queue
from typing import List
INFINITY = 65535


class GraphArray(object):
    def __init__(self):
        self.nv = 0     # 节点数量
        self.ne = 0     # 边数量
        self.graph = []
        self.visited = []

    def create_graph(self, nv: int, ne: int, edges: List[List[int]]):
        """
        :param nv: 节点数
        :param ne: 边数
        :param edges: [[头节点，尾节点，权重], [头节点，尾节点，权重]...]
        :return:
        """
        self.nv = nv
        self.ne = ne

        for i in range(self.nv):
            self.graph.append([INFINITY for _ in range(self.nv)])
            self.graph[i][i] = 0
            self.visited.append(False)

        for edge in edges:
            self.graph[edge[0]][edge[1]] = edge[2]

    def visit(self, v: int):
        print(f'Visited node: {v}')
        self.visited[v] = True

    def is_visited(self, v: int):
        return self.visited[v]

    def init_visit(self):
        for v in range(self.nv):
            self.visited[v] = False

    def is_edge(self, v: int, w: int):
        return self.graph[v][w] < INFINITY

    def insert_edge(self, edge: List[int]):
        """
        插入一条边
        :param edge: [头顶点, 尾顶点, 权重]
        """
        self.graph[edge[0]][edge[1]] = edge[2]

    # 1. 广度优先遍历
    def broad_first_search(self, node: int):
        q = Queue()

        self.visit(node)
        q.put(node)

        while not q.empty():
            v = q.get()
            for w in range(self.nv):
                if self.is_edge(v, w) and not self.visited[w]:
                    self.visit(w)
                    q.put(w)

    # 2. 深度优先遍历
    def deep_first_search(self, node: int):
        self.visit(node)

        for w in range(self.nv):
            if self.is_edge(node, w) and not self.visited[w]:
                self.deep_first_search(w)

    # 3. 无权图的单源最短路径
    def unweighted(self, dist: List[int], path: List[int], s: int):
        """
        :param dist: 保存v到s的距离
        :param path: 保存上一个点的位置
        :param s: 源
        :return:
        """
        q = Queue()
        for _ in range(self.nv):
            dist.append(-1)
            path.append(-1)

        dist[s] = 0
        q.put(s)

        while not q.empty():
            v = q.get()
            for w in range(self.nv):
                if dist[w] == -1 and self.is_edge(v, w):
                    dist[w] = dist[v] + 1
                    path[w] = v
                    q.put(w)

    # 4. 有权图的单源最短路径
    def find_min_dist(self, dist: List[int], collected: List[int]):
        """

        :param dist: 保存的v到s的距离
        :param collected: 节点被收录的情况
        :return:
        """
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

    def dijkstra(self, dist: List[int], path: List[int], s: int):
        """
        :param dist:
        :param path:
        :param s:
        :return:
        """
        collected = []
        for v in range(self.nv):
            collected.append(False)
            dist.append(self.graph[s][v])
            if dist[v] < INFINITY:
                path.append(s)
            else:
                path.append(-1)
            collected[v] = False

        collected[s] = True
        dist[s] = 0

        while True:
            v = self.find_min_dist(dist, collected)
            if v is None:
                break
            collected[v] = True
            for w in range(self.nv):
                if not collected[w] and self.is_edge(v, w):
                    if dist[w] > dist[v] + self.graph[v][w]:
                        dist[w] = dist[v] + self.graph[v][w]
                        path[w] = v

    def floyd(self, dist: List[List[int]], path: List[List[int]]):
        """
        多源最短路径算法
        :param dist: dist[i][j] i到j的最小长度
        :param path:
        :return:
        """
        for i in range(self.nv):
            for j in range(self.nv):
                dist[i][j] = self.graph[i][j]
                path[i][j] = -1

        for k in range(self.nv):
            for i in range(self.nv):
                for j in range(self.nv):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        path[i][j] = k


if __name__ == '__main__':
    edges = [
        [1, 0, 1],
        [1, 3, 2],
        [1, 2, 3],
        [2, 4, 2],
        [3, 4, 4],
    ]
    g = GraphArray()
    g.create_graph(5, 5, edges)

    g.broad_first_search(1)

    path = []
    dist = []
    g.dijkstra(dist, path, 1)
    print(dist, path)
