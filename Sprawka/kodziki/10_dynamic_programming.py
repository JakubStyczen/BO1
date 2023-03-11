#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Marek Lechowicz

import numpy as np
import random

# def cost_function(a, d, q, y, phase):
#     # obliczenie maksymalnej liczby przedmiotów jaką można zmieścić
#     x = int(y/a[phase])
#     if x > d[phase]:
#         x = d[phase]
#
#     if phase == len(a) - 1:
#         return q[x]
#     else:
#         min_cost = np.inf
#         for possible_x in range(x):
#             cost = q[x] + cost_function(a, d, q, y-a[phase]*x, phase+1)


def dynamic(a, d, q, y):
    # a - waga jednej sztuki
    # d - liczba dostępnych sztuk
    # q - macierz kosztów zabrania odpowiedzniej liczby towarów
    # koszty w formie kary, tzn dla makzymalnej liczby danego towaru koszt wynosi 0
    # y - maksymalna ładowność

    # inicjalizacja x jako macierz None'ów
    # i f jako macierz wartości maksymalnych
    # x_matrix = np.array([[[None] for i in range(y+1)] for j in range(len(d))])
    x_matrix = np.zeros((y+1, len(d)))
    f = np.full((y+1, len(d)), np.inf)

    for j in range(f.shape[1]):
        for i in range(f.shape[0]):
            # indeksowanie dla macierzy wejściowych
            # czyli dal j = 0, input_index = etap końcowy
            input_index = f.shape[1] - j - 1

            # wyliczenie maksymalnej liczby przedmiotów
            x = int(i / a[input_index])
            if x > d[input_index]:
                x = d[input_index]

            # jeśli jest to etap ostatni
            if j == 0:
                x_matrix[i, j] = x
                f[i, j] = q[x, input_index]
            # jeśli nie
            else:
                # sprawdzenie wszyskich możliwych ilości x
                for possible_x in range(x+1):
                    # obliczenie kosztu
                    cost = q[possible_x, input_index] + f[i - a[input_index]*possible_x, j - 1]

                    # sprawdzenie czy koszt jest mniejszy lub równy
                    if cost < f[i, j]:
                        # uaktualnienie
                        x_matrix[i, j] = possible_x
                        f[i, j] = cost

    return x_matrix, f

def get_results(a, y, x_matrix, f):
    free_space = y
    strategy = list()

    for j in range(f.shape[1]-1, -1, -1):

        input_index = f.shape[1] - j - 1
        strategy.append(f"| {int(x_matrix[free_space, j])}: x{input_index} (f={f[free_space, j]})|")
        free_space = int(free_space - a[input_index] * x_matrix[free_space, j])

    return strategy


y = 33
a = np.array([1, 2, 3, 4, 3, 2, 10, 2, 3, 3, 13])
d = np.array([6, 3, 2, 1, 8, 2, 1, 2, 7, 3, 5])
q = np.zeros((np.max(d)+1, len(d)))

for j in range(q.shape[1]):
    for i in range(q.shape[0]):
        if i == 0:
            q[i, j] = random.randint(15, 47)
        else:
            q[i, j] = q[i-1, j] - random.randint(0, 15)
            q[i, j] = max((q[i, j], 0))

print("Maksymalna ładowność: y = ", y, "\nWektor a = \n", a, "\nWektor d = \n", d)
print("Macierz q = \n", q)

ans = dynamic(a, d, q, y)
print(f"\n\nMacierz x = \n{ans[0]} \n\nMacierz f = \n{ans[1]}")
print("\n\n", get_results(a, y, ans[0], ans[1]))



y = 7
a = np.array([1, 2, 3])
d = np.array([6, 3, 2])
q = np.array([[20, 9, 6],
              [18, 6, 2],
              [14, 3, 0],
              [11, 0, 0],
              [7, 0, 0],
              [2, 0, 0],
              [0, 0, 0]])

ans = dynamic(a, d, q, y)
print(f"Macierz x = \n{ans[0]} \n\nMacierz f = \n{ans[1]}")
print("\n\n", get_results(a, y, ans[0], ans[1]))