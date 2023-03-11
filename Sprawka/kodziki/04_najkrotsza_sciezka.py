#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import inf
from typing import Dict

# STARA
# def dijkstra(G, a, s, k):
#     d = dict()
#     p = dict()
#     Q = dict()
#
#     for u in G.keys():
#         d[u] = inf
#         p[u] = None
#         Q[u] = u
#
#     Q.pop(s)
#     d[s] = 0
#     u_last = s
#
#     while Q:
#         for el in Q.values():
#             for u in G[u_last]:
#                 if (d[u_last]+a[u_last][u]) < d[u]:
#                     d[u] = d[u_last]+a[u_last][u]
#                     p[u] = u_last
#
#         mini = inf
#         for u in Q.values():
#             if d[u] < mini:
#                 u_last = u
#                 mini = d[u]
#
#         Q.pop(u_last)
#
#     return d[k], p


def dijkstra(G, a, s):
    d = dict()
    p = dict()
    Q = dict()

    for u in G.keys():
        d[u] = inf
        p[u] = None
        Q[u] = u

    Q.pop(s)
    d[s] = 0
    u_last = s

    while Q:
        for el in Q.values():
            for u in G[u_last]:
                if (d[u_last]+a[u_last][u]) < d[u]:
                    d[u] = d[u_last]+a[u_last][u]
                    p[u] = u_last

        mini = inf
        for u in Q.values():
            if d[u] < mini:
                u_last = u
                mini = d[u]

        Q.pop(u_last)

    return d, p


def bellman_ford(G, a, s):
    cost_of_reaching = {i: inf for i in G.keys()}
    previous = {i: -1 for i in G.keys()}

    cost_of_reaching[s] = 0

    for i in range(len(G) - 1):
        for u in G.keys():
            for v in G[u]:
                if cost_of_reaching[v] > cost_of_reaching[u] + a[u][v]:
                    cost_of_reaching[v] = cost_of_reaching[u] + a[u][v]
                    previous[v] = u

    for u in G.keys():
        for v in G[u]:
            if cost_of_reaching[v] > cost_of_reaching[u] + a[u][v]:
                print("Negative cycle exists")
                return None, None
    return cost_of_reaching, previous


def johnson(G, a):

    # dodanie dodatkowego wierzchołka
    keys = list(G.keys())
    additional_node = keys[-1] + 1 # o jeden więcej niż ostatni wierzchołek
    G[additional_node] = G.keys()

    # zabronienie połączeń z wszytkich wierzchołków do nowego wierzołka
    for el in a:
        el.append(inf)

    # dodanie połączeń z nowego wierzołka do wszytkich wierzchołków
    a.append([0 for i in G.keys()])
    # usunięcie połączenie wierzchołka dodanego z samym sobą ()
    a[-1][-1] = inf

    # wywołanie algorytmu Bellmana-Forda oraz sprawdzenie istninia ew. cykli ujemnych
    cost_of_reaching, previous = bellman_ford(G, a, additional_node)
    if cost_of_reaching is None and previous is None:
        print("Negative cycle exists")
        return None

    # modyfikacja wag krawędzi
    for i in range(len(a[0])):
        for j in range(len(a)):
            if a[i][j] != inf:
                a[i][j] = a[i][j] + cost_of_reaching[i] - cost_of_reaching[j]

    # usunięcie dodatkowego wierzchołka
    G.pop(additional_node)
    # usunięcie połączeń z nowego wierzołka do wszytkich wierzchołków
    a.pop(-1)
    # usunięcie połączeń z wszytkich wierzchołków do nowego wierzołka
    for el in a:
        el.pop(-1)

    D = dict()
    for node in G.keys():
        D[node] = dijkstra(G, a, node)
        for destination in D[node][0].keys():
            # wyznaczenie długości dla grafu G
            D[node][0][destination] += - cost_of_reaching[node] + cost_of_reaching[destination]

    return D


def path(D: dict(), start, end):
    D = D[start][1]
    path = [end]
    current = end
    while current != start:
        current = D[current]
        path.append(current)
    return path[::-1]

graph = {
    0: [1, 2, 3, 4],
    1: [0, 3, 6],
    2: [0, 3, 4, 5],
    3: [0, 1, 2, 5, 6],
    4: [0, 2, 5],
    5: [2, 3, 4, 6],
    6: [1, 3, 5]
}

print(path(graph, 0, 6))

# a = [[inf, 2, 1, 4, 3, inf, inf],
#      [2, inf, inf, 3, inf, inf, 5],
#      [1, inf, inf, 7, 1, 2, inf],
#      [4, 3, 7, inf, inf, 4, 4],
#      [3, inf, 1, inf, inf, 3, inf],
#      [inf, inf, 2, 4, 3, inf, 3],
#      [inf, 5, inf, 4, inf, 3, inf]]
#
# graph2 = {
#     0: [1],
#     1: [3, 4],
#     2: [0, 1],
#     3: [4, 5],
#     4: [2, 5],
#     5: [0, 2]
# }
#
# a2 = [[inf, 5, inf, inf, inf, inf],
#      [inf, inf, inf, 3, 9, inf],
#      [3, -4, inf, inf, inf, inf],
#      [inf, inf, inf, inf, 3, 2],
#      [inf, inf, -1, inf, inf, -5],
#      [9, inf, 8, inf, inf, inf]]
#
# graph3 = {
#     0: [1, 3],
#     1: [0, 2],
#     2: [0],
#     3: [0, 2]
# }
#
# a3 = [[inf, -3, inf, 2],
#       [5, inf, 3, inf],
#       [1, inf, inf, inf],
#       [-1, inf, 4, inf]]
#
# graph_negative = {
#     0: [1, 2, 3, 4],
#     1: [0, 3, 6],
#     2: [0, 3, 4, 5],
#     3: [0, 1, 2, 5, 6],
#     4: [0, 2, 5],
#     5: [2, 3, 4, 6],
#     6: [1, 3, 5, 9],
#     7: [6],
#     8: [6, 7],
#     9: [8]
# }
#
# a_negative = [
#      [inf, 2, 1, 4, 3, inf, inf, inf, inf, inf],
#      [2, inf, inf, 3, inf, inf, 5, inf, inf, inf],
#      [1, inf, inf, 7, 1, 2, inf, inf, inf, inf],
#      [4, 3, 7, inf, inf, 4, 4, inf, inf, inf],
#      [3, inf, 1, inf, inf, 3, inf, inf, inf, inf],
#      [inf, inf, 2, 4, 3, inf, 3, inf, inf, inf],
#      [inf, 5, inf, 4, inf, 3, inf, inf, inf, 0],
#      [inf, inf, inf, inf, inf, inf, 4, inf, inf, inf],
#      [inf, inf, inf, inf, inf, inf, -1, 4, inf, inf],
#      [inf, inf, inf, inf, inf, inf, inf, inf, -1, inf]
# ]
#
# #print(dijkstra(graph, a, 0))
# #print(bellman_ford(graph2, a2, 0))
# D = johnson(graph_negative, a_negative)

# print(path(D, 0, 8))