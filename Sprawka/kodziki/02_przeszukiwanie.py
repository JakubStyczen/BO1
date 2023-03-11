#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Dict, List



def dfs(G: Dict[int, List[int]], s: int):
    # No - lista kolejno odwiedzonych, czyli ponumerowanych wierzcholków
    # wierzchłek na początu listy ma numer 1, kolejny 2 itd.
    No = list()

    # zmienna opisująca istnienie cykli - domyślnie zakładamy graf acykliczny
    cycle_exists = False

    # zmienna opisująca spójność - domyślnie zakładamy graf spójy
    is_consistent = True

    stos = list()   # utworzenie zmiennej stos - bufor LIFO
    stos.append(s)  # odłożenie na stos wierzchołka startowego
    while stos:     # dopóki są elementy w stosie wykonuj:
        v = stos.pop()  # zdejmij ostatni element ze stosu
        if v not in No:     # jeżeli wierzchołek nie został ponumerowany wykonaj:
            No.append(v)    # dodaj wierzchołek do listy - nadaj mu numer

            no_of_neighbours_visited = 0    # liczba sąsiadów "v", którzy już zostali ponumerowani
            for u in G[v][::-1]:  # dla każdego "u" w liście sąsiedztwa "v"
                stos.append(u)    # odłóż "u" na stos
                if u in No:       # jeżeli "u" otrzymało numer
                    no_of_neighbours_visited += 1   # zwiększ o 1 liczbę odwiedzonych sąsiadów
                    if no_of_neighbours_visited > 1:    # jeżeli liczna już odwiedzonych sąsiadów przekracza 1
                        cycle_exists = True     # zaznacz, że istnieje cykl
    # sprawdzenie spójności
    if len(No) < len(G.keys()):     # jeżeli liczba wierzchołków ponumerowanych
                                    # jest mniejsza niż liczba kluczy w słowniku
        is_consistent = False       # zaznac, że graf nie jest spójny
    # zwróć krotkę zawierającą:
    # 1) listę odwiedzonych wierzchołków - nowy numer odpowiada pozycji na liście
    # 2) zmienną typu bool stwierdzjącą czy istnieją cykle
    # 3) zmienną typu bool stwierdzjącą czy graf jest spójny
    return No, cycle_exists, is_consistent

def DFS(G: Dict[int, List[int]], s: int):
    # No - lista kolejno odwiedzonych, czyli ponumerowanych wierzcholków
    # wierzchłek na początu listy ma numer 1, kolejny 2 itd.
    No = list()

    # zmienna opisująca istnienie cykli - domyślnie zakładamy graf acykliczny
    cycle_exists = False

    # zmienna opisująca spójność - domyślnie zakładamy graf spójy
    is_consistent = True

    stos = list()   # utworzenie zmiennej stos - bufor LIFO
    stos.append(s)  # odłożenie na stos wierzchołka startowego
    while stos:     # dopóki są elementy w stosie wykonuj:
        v = stos.pop()  # zdejmij ostatni element ze stosu
        No.append(v)    # dodaj wierzchołek do listy - nadaj mu numer

        no_of_neighbours_visited = 0    # liczba sąsiadów "v", którzy już zostali ponumerowani
        for u in G[v][::-1]:  # dla każdego "u" w liście sąsiedztwa "v"

            if u in No:       # jeżeli
                no_of_neighbours_visited += 1
                if no_of_neighbours_visited > 1:
                    cycle_exists = True
            elif u not in stos:
                stos.append(u)  # odłóż "u" na stos

    if len(No) < len(G.keys()):
        is_consistent = False
    return No, cycle_exists, is_consistent





graph = {
    1: [2],
    2: [1, 3],
    3: [2, 7],
    4: [5, 7],
    5: [4, 6],
    6: [5],
    7: [3, 4, 8, 9],
    8: [7, 9],
    9: [7, 8, 10],
    10: [9]
}

sa = {
    1: [2],
    2: [1, 3, 4],
    3: [2],
    4: [2, 5],
    5: [4, 6],
    6: [5]
}

sc = {
    1: [2],
    2: [1, 3, 4],
    3: [2, 5, 6],
    4: [2, 5],
    5: [3, 4, 6],
    6: [3, 5]
}

ac = {
    1: [2],
    2: [1, 4],
    3: [5, 6],
    4: [2],
    5: [3, 6],
    6: [3, 5]
}

# print(dfs(graph, 3))
# print(DFS(graph, 3))
ans1 = dfs(sa, 4)

wynik1 = "1: " + str(ans1[0][0])
for i in range(1, len(ans1[0])):
    wynik1 += ", " + str(i+1) + ": " + str(ans1[0][i])

wynik1 += "\nCycle exists: " + str(ans1[1])
wynik1 += "\nGraph is consistent: " + str(ans1[2])

print(wynik1)

ans2 = dfs(sc, 4)

wynik2 = "1: " + str(ans2[0][0])
for i in range(1, len(ans2[0])):
    wynik2 += ", " + str(i+1) + ": " + str(ans2[0][i])

wynik2 += "\nCycle exists: " + str(ans2[1])
wynik2 += "\nGraph is consistent: " + str(ans2[2])

print(wynik2)

ans3 = dfs(ac, 5)

wynik3 = "1: " + str(ans3[0][0])
for i in range(1, len(ans3[0])):
    wynik3 += ", " + str(i+1) + ": " + str(ans3[0][i])

wynik3 += "\nCycle exists: " + str(ans3[1])
wynik3 += "\nGraph is consistent: " + str(ans3[2])

print(wynik3)