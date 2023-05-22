import numpy as np


class Vertex:
    def __init__(self, data):
        self.key = data

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)


class Edge:
    def __init__(self, capacity, is_residual=False):
        self.capacity = capacity
        self.is_residual = is_residual
        self.residual = capacity
        self.flow = 0

    def __str__(self):
        return str(self.capacity) + " " + str(self.flow) + " " + str(self.residual) + " " + str(self.is_residual)


class GraphMatrix:
    def __init__(self):
        self.v_list = []
        self.dicto = {}
        self.graph = []
        self.ssize = 0

    def get_vertex_idx(self, vertex):
        return self.dicto[vertex]

    def get_vertex(self, vertex_idx):
        for key, value in self.dicto.items():
            if value == vertex_idx:
                return key

    def insert_vertex(self, vertex: Vertex):
        self.v_list.append(vertex)
        self.dicto[vertex] = len(self.v_list) - 1
        if len(self.graph) == 0:
            self.graph.append([0])
        else:
            for line in self.graph:
                line.append(0)
            self.graph.append([0 for i in range(len(self.graph[0]))])

    def insert_edge(self, v1, v2, edge: Edge):
        if v1 not in self.v_list:
            self.insert_vertex(v1)
        if v2 not in self.v_list:
            self.insert_vertex(v2)
        idx1 = self.get_vertex_idx(v1)
        idx2 = self.get_vertex_idx(v2)
        self.graph[idx1][idx2] = edge
        self.ssize += 1

    def delete_edge(self, v1, v2):
        idx1 = self.get_vertex_idx(v1)
        idx2 = self.get_vertex_idx(v2)
        self.graph[idx1][idx2] = 0
        self.ssize -= 1

    def upgrade_dict(self):
        for i in range(len(self.v_list)):
            self.dicto[self.v_list[i]] = i

    def delete_vertex(self, vertex):
        idx = self.get_vertex_idx(vertex)
        self.v_list.remove(vertex)
        self.dicto.pop(vertex)
        self.upgrade_dict()
        self.graph.pop(idx)
        for line in self.graph:
            line.pop(idx)

    def neighbours(self, v_idx):
        result_list = []
        for i in range(len(self.graph[v_idx])):
            if not self.graph[v_idx][i] == 0:
                result_list.append((i, self.graph[v_idx][i]))
        return result_list

    def size(self):
        return self.ssize

    def order(self):
        return len(self.graph)

    def edges(self):
        result_list = []
        for row in range(len(self.graph)):
            for col in range(row):
                if not self.graph[row][col] == 0:
                    result_list.append((self.get_vertex(row).key, self.get_vertex(col).key))
        return result_list

    def bfs(self, s):
        visited = {s: None}
        unvisited = [s]
        while unvisited:
            v = unvisited.pop()
            for el, w in self.neighbours(v):
                if el not in visited.keys() and w.residual > 0:
                    unvisited.insert(0, el)
                    visited[el] = v
        return visited

    def analiz(self, s, k, parent_list):
        v = k
        min_capa = np.inf
        try:
            c = parent_list[v]
        except KeyError:
            return 0
        while v != s:
            parent = parent_list[v]
            edge = self.graph[parent][v]
            if edge.residual < min_capa:
                min_capa = edge.residual
            v = parent
        return min_capa

    def aug_path(self, s, k, parent_list, min_capa):
        v = k
        try:
            c = parent_list[v]
        except KeyError:
            return None
        while v != s:
            parent = parent_list[v]
            edge = self.graph[parent][v]
            virtual = self.graph[v][parent]
            edge.flow += min_capa
            edge.residual -= min_capa
            virtual.residual += min_capa
            v = parent

    def main_fun(self,s,k):
        sum = 0
        parent_list = self.bfs(s)
        min_c = self.analiz(s, k, parent_list)
        while min_c > 0:
            self.aug_path(s, k, parent_list, min_c)
            parent_list = self.bfs(s)
            min_c = self.analiz(s, k, parent_list)
        for i in range(len(self.graph)):
            if self.graph[i][k] != 0:
                sum += self.graph[i][k].flow
        return sum


def printgraph(g):
    n = g.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = g.get_vertex(i).key
        print(v, end=" -> ")
        nbrs = g.neighbours(i)
        for (j, w) in nbrs:
            print(g.get_vertex(j).key, w, end=";")
        print()
    print("-------------------")


graf_0 = [ ('s','u',2), ('u','t',1), ('u','v',3), ('s','v',1), ('v','t',2)]
#3
graf_1 = [ ('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9), ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4) ]
#23
graf_2 = [ ('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6), ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
#5
graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7), ('d', 'c', 4)]
#6
k = [2, 4, 6, 4]
g = [graf_0, graf_1, graf_2, graf_3]
for i in range(4):
    graf = g[i]
    test = GraphMatrix()
    for el in graf:
        v1 = Vertex(el[0])
        v2 = Vertex(el[1])
        edge = Edge(el[2])
        res_edge = Edge(0, True)
        test.insert_edge(v1,v2,edge)
        if test.graph[test.get_vertex_idx(v2)][test.get_vertex_idx(v1)] == 0:
            test.insert_edge(v2, v1, res_edge)
    print(test.main_fun(0,k[i]))
    printgraph(test)
