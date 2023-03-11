#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import random

def johnson2(t, just_ordering=False):
    # szeregownie
    optimal_t = np.zeros(t.shape)
    crossed = list()
    first = 0
    last = -1
    # zakładam, że w pierwszym wierszu znajdują się numery kolejnych zadań
    for k in range(len(t[0])):
        min_t = np.inf
        for i in range(1, 3):
            for j in range(len(t[0])):
                # znaleznienei minimum
                if (t[i, j] < min_t) and (j not in crossed):
                    min_t = t[i, j]
                    argmin_t = (i, j)

        if argmin_t[0] == 1:
            # wstawienie na początek
            optimal_t[0][first] = t[0][argmin_t[1]]
            optimal_t[1][first] = t[1][argmin_t[1]]
            optimal_t[2][first] = t[2][argmin_t[1]]
            first += 1
            crossed.append(argmin_t[1])

        elif argmin_t[0] == 2:
            # wstawienie na koniec
            optimal_t[0][last] = t[0][argmin_t[1]]
            optimal_t[1][last] = t[1][argmin_t[1]]
            optimal_t[2][last] = t[2][argmin_t[1]]
            last -= 1
            crossed.append(argmin_t[1])

    # zwrócenie jedynie kolejności zadań
    # do metody johnsona dla 3 maszyn
    if just_ordering:
        return optimal_t[0]

    # obliczanie teminów
    optimal_t[2, 0] += optimal_t[1, 0]
    for j in range(len(optimal_t[0])):
        if j != 0:
            optimal_t[1, j] += optimal_t[1, j-1]
            optimal_t[2, j] += max(optimal_t[1, j], optimal_t[2, j-1])

    return optimal_t

    # EW. do johnsona 3
    # optimal_t = t.copy()
    # i = 0
    # for task in ordering:
    #     id = int(np.argwhere(t[0] == task))
    #     optimal_t[:, i] = t[:, id]
    #     i += 1
    #
    # print(optimal_t)
    #
    # # obliczanie teminów
    # optimal_t[2, 0] += optimal_t[1, 0]
    # optimal_t[3, 0] += optimal_t[2, 0]
    # for j in range(len(optimal_t[0])):
    #     if j != 0:
    #         optimal_t[1, j] += optimal_t[1, j - 1]
    #         optimal_t[2, j] += max(optimal_t[1, j], optimal_t[2, j - 1])
    #         optimal_t[3, j] += max(optimal_t[2, j], optimal_t[3, j - 1])

def johnson3(t):
    if max(t[1]) < max(t[2]) and max(t[3]) < max(t[2]):
        raise ValueError("Johnson rule's condition not satisfied!")

    t_temp = np.array([t[0], t[1]+t[2], t[2]+t[3]])
    ordering = johnson2(t_temp, just_ordering=True)

    return order(t, ordering)

def order(t, ordering):
    optimal_t = t.copy()
    i = 0
    for task in ordering:
        id = int(np.argwhere(t[0] == task))
        optimal_t[:, i] = t[:, id]
        i += 1

    # obliczanie teminów
    for i in range(2, optimal_t.shape[0]):
        optimal_t[i, 0] += optimal_t[i-1, 0]

    for j in range(len(optimal_t[0])):
        if j != 0:
            optimal_t[1, j] += optimal_t[1, j - 1]
            for i in range(2, optimal_t.shape[0]):
                optimal_t[i, j] += max(optimal_t[i-1, j], optimal_t[i, j - 1])

    return optimal_t

def CDS(t):
    min_t = np.inf
    for r in range(1, t.shape[0]):
        # utworzenie problemu pomocniczego
        temp_t = np.array([t[0], np.sum(t[1:r+1], axis=0), np.sum(t[-r:], axis=0)])

        # wykonanie dla tego problemu algorytmu Johnsona
        candidate_ordering = johnson2(t, just_ordering=True)
        candidate_t = order(t, candidate_ordering)

        # sprawdzenie czy jest to najlepsze z dotychczasowych rozwiązań
        if candidate_t[candidate_t.shape[0]-1, candidate_t.shape[1]-1] < min_t:
            optimal_t = candidate_t
            min_t = candidate_t[candidate_t.shape[0]-1, candidate_t.shape[1]-1]

    return optimal_t

t0 = np.array([[1, 2, 3, 4, 5, 6],
              [9, 6, 8, 7, 12, 3],
              [7, 3, 5, 10, 4, 7]])

t1 = np.array([[1, 2, 3, 4, 5],
               [7, 11, 8, 7, 6],
               [6, 5, 3, 5, 3],
               [4, 12, 7, 8, 3]])

t2 = np.array([[1, 2, 3, 4, 5],
               [12, 7, 10, 4, 16],
               [10, 12, 6, 15, 8],
               [6, 18, 8, 13, 6],
               [15, 9, 12, 7, 10]])

random_list = random.sample(range(0, 88), 5*12)
t = np.zeros((6, 12))
t[0] = np.arange(1, 13)
for i in range(1, t.shape[0]):
    temp = random_list[12*(i-1):12*i]
    t[i] = temp

# print(f"Uszeregowanie początkowe: \n{t} \n\nUszeregowanie końcowe:\n{johnson2(t)}")
# print(f"Uszeregowanie początkowe: \n{t1} \n\nUszeregowanie końcowe:\n{johnson3(t1)}")
print(f"Uszeregowanie początkowe: \n{t2} \n\nUszeregowanie końcowe:\n{CDS(t2)}")
# print(f"Uszeregowanie początkowe: \n{t} \n\nUszeregowanie końcowe:\n{CDS(t)}")