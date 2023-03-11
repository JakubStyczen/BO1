#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import inf
from typing import Dict, List

def DPA(G: Dict, a: List[List], s: int):
    # utworzenie sumy i zbiorów A i Q oraz list alfa i beta (01 - 06)
    suma = 0
    A = list()
    alfa = [0 for i in range(len(G))]
    beta = [inf for i in range(len(G))]
    Q = [i for i in range(len(G))]

    # zdjęcie z Q wierzchołka s oraz przypisanie mu kosztu 0 (07 - 08)
    beta[s] = 0
    Q.remove(s)

    # ustawienie s jako ostatnio wybranego wierzchołka (09)
    u_last = s

    # pętla główna (10)
    while Q:
        for el in Q:  # dla każdego u należącego do Q (11)
            for u in G[u_last]:  # i każdego u należącego do N[u*] (11)
                # jeśli a[u,u*]<beta[u] to alfa[u] ←u*; beta[u]←a[u,u*] (12)
                if a[u][u_last] < beta[u]:
                    alfa[u] = u_last
                    beta[u] = a[u][u_last]

        # dla każdegou u∈Q u*←arg min(beta[u]) (13 - 14)
        # poszukiwanie miniumum może sugerować użycie wbudowanej funkcji min()
        # jednak powoduje to problmy, ponieważ szukamy wtedy minimum z całego
        # beta, więc domyślnie zawsze będziemy znajdować wierzchołek startowy
        # o koszcie dotarcia 0
        mini = inf
        for u in Q:
            if beta[u] < mini:
                mini = beta[u]
                u_last = u

        # usunięcie z Q u*,
        # dodanie do A kolejnej krawędzi,
        # zwiększenie sumy (15 - 17)
        Q.remove(u_last)
        A.append((alfa[u_last], u_last))
        suma += a[alfa[u_last]][u_last]

    # (18)
    return A, suma


# definicja grafu, macierzy kosztów oraz wywołanie funkcji
graph = {
    0: [1, 2, 3, 4],
    1: [0, 3, 6],
    2: [0, 3, 4, 5],
    3: [0, 1, 2, 5, 6],
    4: [0, 2, 5],
    5: [2, 3, 4, 6],
    6: [1, 3, 5]
}

a = [[inf, 2, 1, 4, 3, inf, inf],
     [2, inf, inf, 3, inf, inf, 5],
     [1, inf, inf, 7, 1, 2, inf],
     [4, 3, 7, inf, inf, 4, 4],
     [3, inf, 1, inf, inf, 3, inf],
     [inf, inf, 2, 4, 3, inf, 3],
     [inf, 5, inf, 4, inf, 3, inf]]

graph2 = {
    0: [1, 2, 4],
    1: [0],
    2: [0, 4],
    3: [5, 6],
    4: [0, 5],
    5: [3, 6],
    6: [3, 5]
}

a2 = [[inf, 2, 1, inf, 3, inf, inf],
     [2, inf, inf, inf, inf, inf, inf],
     [1, inf, inf, inf, 1, inf, inf],
     [inf, inf, inf, inf, inf, 4, 4],
     [3, inf, 1, inf, inf, inf, inf],
     [inf, inf, inf, 4, inf, inf, 3],
     [inf, inf, inf, 4, inf, 3, inf]]

graph3 = {
    0: [1, 2, 3, 4],
    1: [0, 3],
    2: [0, 3, 4, 5],
    3: [0, 1, 2, 5],
    4: [0, 2, 5],
    5: [2, 3, 4],
    6: [1, 3, 5]
}

a3 = [[inf, 2, 1, 4, 3, inf, inf],
     [2, inf, inf, 3, inf, inf, inf],
     [1, inf, inf, 7, 1, 2, inf],
     [4, 3, 7, inf, inf, 4, inf],
     [3, inf, 1, inf, inf, 3, inf],
     [inf, inf, 2, 4, 3, inf, inf],
     [inf, 5, inf, 4, inf, 3, inf]]

#print(DPA(graph, a, 0))
# print(DPA(graph2, a2, 0))
print(DPA(graph3, a3, 0))
