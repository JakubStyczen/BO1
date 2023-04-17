import networkx as nx
import matplotlib.pyplot as plt

def pert(graph):
    # Topological sort
    topological_order = list(nx.topological_sort(graph))
    
    # Earliest start time
    earliest_start_time = {node: 0 for node in topological_order}
    for node in topological_order:
        for neighbor in graph.neighbors(node):
            earliest_start_time[neighbor] = max(earliest_start_time[neighbor], earliest_start_time[node] + graph[node][neighbor]['weight'])

    # Latest start time
    latest_start_time = {node: earliest_start_time[node] for node in topological_order[::-1]}
    for node in topological_order[::-1]:
        for neighbor in graph.neighbors(node):
            latest_start_time[node] = min(latest_start_time[node], latest_start_time[neighbor] - graph[node][neighbor]['weight'])
    
    # Critical path
    critical_path = []
    for node in topological_order:
        for neighbor in graph.neighbors(node):
            if earliest_start_time[node] + graph[node][neighbor]['weight'] == earliest_start_time[neighbor] and latest_start_time[node] == latest_start_time[neighbor] - graph[node][neighbor]['weight']:
                critical_path.append(node)
    
    # Return results
    return latest_start_time[1], critical_path

# Test example graph with 10 vertices and 20 edges
G = nx.DiGraph()
G.add_nodes_from(range(1, 11))
G.add_edges_from([(1, 2, {'weight': 4}), (1, 3, {'weight': 2}), (2, 4, {'weight': 5}), (2, 5, {'weight': 3}),
                  (3, 4, {'weight': 4}), (3, 5, {'weight': 2}), (4, 6, {'weight': 3}), (4, 7, {'weight': 5}),
                  (5, 6, {'weight': 4}), (5, 7, {'weight': 3}), (6, 8, {'weight': 2}), (6, 9, {'weight': 4}),
                  (7, 8, {'weight': 4}), (7, 9, {'weight': 2}), (8, 10, {'weight': 6}), (9, 10, {'weight': 4}),
                  (1, 4, {'weight': 1}), (1, 5, {'weight': 3}), (3, 6, {'weight': 1}), (3, 7, {'weight': 3})])

# Compute PERT
termination_time, critical_path = pert(G)

# Print results
print("Termination time (days):", termination_time)
print("Critical path:", critical_path)

# Visualize graph with critical path highlighted
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=500)
nx.draw_networkx_labels(G, pos, font_size=16, font_weight="bold")
nx.draw_networkx_edges(G, pos, width=2, edge_color="gray")
nx.draw_networkx_edges(G, pos, edgelist=[(critical_path[i], critical_path[i+1]) for i in range(len(critical_path)-1)], width=4, edge_color="red")
plt.axis("off")
plt.show()