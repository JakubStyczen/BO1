#skończone
    
inf = float('inf')

class Graph:
    def __init__(self):
        self.vertex_dict = {}
    
    def isEmpty(self):
        return True if self.vertex_dict else False

    def insertVertex(self, v):
        self.vertex_dict[v] = self.order()
    
    def deleteVertex(self, removed_idx):
        for v, idx in self.vertex_dict.items():
            if idx == removed_idx:
                del self.vertex_dict[v]
                break
    
    def deleteEdge(self):
        pass
    
    def getVertexIdx(self, v):
        return self.vertex_dict[v]
        
    def getVertex(self, v_idx):
        for v, idx in self.vertex_dict.items():
            if idx == v_idx:
                return v 
    
    def order(self):
        return len(self.vertex_dict)
        
    def size(self):
        pass
    
    
class Edge:
    def __init__(self, capacity, isResidual=False):
        self.capacity = capacity
        self.flow = 0
        self.residual = capacity
        self.isResidual = isResidual

    def __str__(self):
        return f'{self.capacity} {self.flow} {self.residual} {self.isResidual}'
        
    def __repr__(self):
        return f'{self.capacity} {self.flow} {self.residual} {self.isResidual}'
    
class Vertex:
    def __init__(self, key):
        self.key = key
        
    def __eq__(self, other):
        return self.key == other.key
    
    def __hash__(self):
        return hash(self.key)
    
    def __str__(self):
        return str(self.key)
    
    def __repr__(self):
        return str(self.key)
        
class NeighborListGraph(Graph):
    def __init__(self):
        super().__init__()
        self.neighbors_dict = {}
        self.test = 0
        self.weights = {}
    
    def insertVertex(self, v):
        super().insertVertex(v)
        self.neighbors_dict[self.vertex_dict[v]] = []
    
    def insertEdge(self, v_start, v_end, weight=None):
        if v_start not in self.vertex_dict:
            self.insertVertex(v_start)
        if v_end not in self.vertex_dict:
            self.insertVertex(v_end)
        start_id, end_id = self.getVertexIdx(v_start), self.getVertexIdx(v_end)
        if end_id not in self.neighbors_dict[start_id]:
            self.neighbors_dict[start_id].append(end_id)
            self.neighbors_dict[start_id].sort()
        # if start_id not in self.neighbors_dict[end_id]:
        #     self.neighbors_dict[end_id].append(start_id)
        #     self.neighbors_dict[end_id].sort()
        # if (start_id, end_id) not in self.weights:
        self.weights[(start_id, end_id)] = weight
        
    def deleteEdge(self, v_start, v_end):
        start_id, end_id = self.getVertexIdx(v_start), self.getVertexIdx(v_end)
        if start_id in self.neighbors_dict[end_id]:
            self.neighbors_dict[end_id].remove(start_id)
        if end_id in self.neighbors_dict[start_id]:
            self.neighbors_dict[start_id].remove(end_id)
        
    
    def deleteVertex(self, v):
        removed_idx = self.getVertexIdx(v)
        super().deleteVertex(removed_idx)
        del self.neighbors_dict[removed_idx]
        
        #delete v_idx from neighbors_dict
        for ends in self.neighbors_dict.values():
            if removed_idx in ends:
                ends.remove(removed_idx)
                
        #decrese idxs > rm_idx by 1
        for v, idx in self.vertex_dict.items():
            if idx == removed_idx:
                del self.vertex_dict[v]
            if idx > removed_idx:
                self.vertex_dict[v] = idx - 1
                
        #update dict for deleted        
        updated = {}
        for v_idx, ends in self.neighbors_dict.items():
            new_ends = []
            for end in ends:
                if v_idx > removed_idx:
                    new_ends.append(end-1)
                else:
                    new_ends.append(end)
            if v_idx > removed_idx:
                updated[v_idx-1] = new_ends
            else:
                updated[v_idx] = new_ends
        self.neighbors_dict = updated
        
    def size(self):
        return len(self.edges())
    
    def _edges(self):
        res = []
        for start, ends in self.neighbors_dict.items():
            for end in ends:
                v_start = self.getVertex(start)
                v_end = self.getVertex(end)
                if (v_start.key, v_end.key) not in res or (v_end.key, v_start.key) not in res:
                    res.append((v_start.key, v_end.key))
        return res
        
    def edges(self):
        res = []
        for start, ends in self.neighbors_dict.items():
            for end in ends:
                if (start, end) not in res or (end, start) not in res:
                    res.append((start, end))
        return res

    def neighbors(self, vertex_idx):
        v = self.getVertex(vertex_idx)
        return self.neighbors_dict[v]
        
    def neighborsIdx(self, vertex_idx):
        return self.neighbors_dict[vertex_idx]
        
    def neighbours(self, vertex_idx):
        return [(u, self.weights[(vertex_idx), u]) for u in self.neighbors_dict[vertex_idx]]
        
    def BFS(self, start):
        Q = [start]
        parents = {v: None for v in self.vertex_dict.values()}
        visited = []
        while Q:
            v = Q.pop(0)
            for u, weight in self.neighbours(v):
                if u not in visited and weight.residual > 0:
                    Q.append(u)
                    visited.append(u)
                    parents[u] = v
        return parents
        
    def find_bottleneck(self, start_idx, end_idx, parents):
        if parents[end_idx] is None:
            return 0
        
        current_vertex = end_idx
        current_bottleneck = inf
        
        while current_vertex != start_idx:
            current_edge = self.weights[(parents[current_vertex], current_vertex)]
            current_bottleneck = current_edge.residual if current_edge.residual < current_bottleneck else current_bottleneck
            current_vertex = parents[current_vertex]
        return current_bottleneck
    
    def augment_path(self, start_idx, end_idx, parents, bottleneck):
        current_vertex = end_idx

        
        while current_vertex != start_idx:
            current_parent = parents[current_vertex]
            current_edge = self.weights[(current_parent, current_vertex)]
            backward_edge = self.weights[(current_vertex, current_parent)]
            
            #update flow and residual
            current_edge.flow += bottleneck
            current_edge.residual -= bottleneck
            backward_edge.residual += bottleneck
            current_vertex = current_parent
            
        
    def FordFulkerson(self, s, k):
        start_idx = self.getVertexIdx(s)
        end_idx = self.getVertexIdx(k)
        
        max_flow = 0
        parents = self.BFS(start_idx)
        bottleneck = self.find_bottleneck(start_idx, end_idx, parents)
        while bottleneck > 0:
            self.augment_path(start_idx, end_idx, parents, bottleneck)
            parents = self.BFS(start_idx)
            bottleneck = self.find_bottleneck(start_idx, end_idx, parents)
        for _, weight in self.neighbours(end_idx):
            max_flow += weight.residual
        
        return max_flow
        
    
def printgraph(g):
    n = g.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = g.getVertex(i).key
        print(v, end=" -> ")
        nbrs = g.neighbours(i)
        for (j, w) in nbrs:
            print(g.getVertex(j).key, w, end=";")
        print()
    print("-------------------")
        
if __name__ == "__main__":
    graf_0 = [ ('s','u',2), ('u','t',1), ('u','v',3), ('s','v',1), ('v','t',2)]
    #3
    graf_1 = [ ('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9), ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4) ]
    #23
    graf_2 = [ ('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6), ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    #5
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7), ('d', 'c', 4)]
    #6
    
    for i, g in enumerate([graf_0, graf_1, graf_2, graf_3]):
        new_graph = NeighborListGraph()
        for v in g:
            v1, v2 = Vertex(v[0]), Vertex(v[1])
            edge,  residual = Edge(v[2]), Edge(0, True)
            new_graph.insertEdge(v1,v2, edge)
            if (v[1], v[0]) not in new_graph._edges():
                new_graph.insertEdge(v2, v1, residual)
        print(new_graph.FordFulkerson(Vertex('s'), Vertex('t')))
        printgraph(new_graph)
            
            