import polska

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
    
class Vertex:
    def __init__(self, key):
        self.key = key[2]
        self.data = key[:2]
        
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
    
    def insertVertex(self, v):
        super().insertVertex(v)
        self.neighbors_dict[self.vertex_dict[v]] = []
    
    def insertEdge(self, v_start, v_end):
        if v_start not in self.vertex_dict:
            self.insertVertex(v_start)
        if v_end not in self.vertex_dict:
            self.insertVertex(v_end)
        start_id, end_id = self.getVertexIdx(v_start), self.getVertexIdx(v_end)
        if end_id not in self.neighbors_dict[start_id]:
            self.neighbors_dict[start_id].append(end_id)
            self.neighbors_dict[start_id].sort()
        if start_id not in self.neighbors_dict[end_id]:
            self.neighbors_dict[end_id].append(start_id)
            self.neighbors_dict[end_id].sort()
        
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
    
    def edges(self):
        res = []
        for start, ends in self.neighbors_dict.items():
            for end in ends:
                v_start = self.getVertex(start)
                v_end = self.getVertex(end)
                if (v_start.key, v_end.key) not in res or (v_end.key, v_start.key) not in res:
                    res.append((v_start.key, v_end.key))
        return res

    def neighbors(self, vertex_idx):
        v = self.getVertex(vertex_idx)
        return self.neighbors_dict[v]
    
    def BFS(self, start):
        Q = [start]
        visited = [start]
        while Q:
            v = Q.pop(0)
            for u in self.neighbors_dict[v]:
                if u not in visited:
                    Q.append(u)
                    visited.append(u)
        return visited
    
    def DFS(self, start):
        S = [start]
        visited = [start]
        while S:
            v = S.pop(len(S)-1)
            for u in self.neighbors_dict[v]:
                if u not in visited:
                    S.append(u)
                    visited.append(u)
        return visited
    
    def graphColoring(self, traverse_type, start):
        if traverse_type == "BFS":
            sequence = self.BFS(start)
        elif traverse_type == "DFS":
            sequence = self.DFS(start)
        else:
            print('Wrong type of graph traversing')
            return
        colors = {}
        V = len(sequence)
        for v in sequence:
            neighbors_colors = set(colors.get(neighbor) for neighbor in self.neighbors_dict[v])
            opts = [col for col in range(V) if col not in neighbors_colors]
            colors[v] = opts[0]
            
        return [(str(lstG.getVertex(u)), color) for u, color in colors.items()]
        
class NeighborMatrixGraph(Graph):
    def __init__(self, placeholder=0):
        super().__init__()
        self.neighbors_maxtrix = [[]]
        self.placeholder = placeholder

    def insertVertex(self, v):
        super().insertVertex(v)
        if not self.neighbors_maxtrix[0]:
            self.neighbors_maxtrix[0].append(self.placeholder)
        else:
            for row in self.neighbors_maxtrix:
                row.append(self.placeholder)
            self.neighbors_maxtrix.append([self.placeholder for _ in range(len(self.neighbors_maxtrix[0]))])

    def insertEdge(self, v_start, v_end, edge=1):
        if v_start not in self.vertex_dict:
            self.insertVertex(v_start)
        if v_end not in self.vertex_dict:
            self.insertVertex(v_end)
        start_id = self.getVertexIdx(v_start)
        end_id = self.getVertexIdx(v_end)
        self.neighbors_maxtrix[start_id][end_id] = edge
        

    def deleteEdge(self, v_start, v_end):
        start_id = self.getVertexIdx(v_start)
        end_id = self.getVertexIdx(v_end)
        self.neighbors_maxtrix[start_id][end_id] = self.placeholder
    
    def deleteVertex(self, v):
        removed_idx = self.getVertexIdx(v)
        super().deleteVertex(removed_idx)
        #delete row with idx
        self.neighbors_maxtrix.pop(removed_idx)
        #delete column
        for row in self.neighbors_maxtrix:
            for idx in range(len(row)):
                if idx == removed_idx:
                    row.pop(removed_idx)

    
    def size(self):
        return len(self.edges())
    
    def neighbors(self, v_idx):
        res = []
        for idx, elem in enumerate(self.neighbors_maxtrix[v_idx]):
            if elem != 0:
                res.append(idx)
        return res
            
    def edges(self):
        res = []
        for i, row in enumerate(self.neighbors_maxtrix):
            for j, elem in enumerate(row):
                if self.neighbors_maxtrix[i][j] != 0:
                    v_start = self.getVertex(i)
                    v_end = self.getVertex(j)
                    if (v_start.key, v_end.key) not in res or (v_end.key, v_start.key) not in res:
                        res.append((v_start.key, v_end.key))
        return res
    
    
if __name__ =="__main__":
    matG = NeighborMatrixGraph()
    lstG = NeighborListGraph()
    for start, end in polska.graf:
        start = Vertex(polska.slownik[start])
        end = Vertex(polska.slownik[end])
        matG.insertEdge(start, end)
        lstG.insertEdge(start, end)
    polska.draw_map(matG.edges(), lstG.graphColoring("BFS", 14))
    # polska.draw_map(lstG.edges(), lstG.graphColoring("DFS", 14))

        
       



