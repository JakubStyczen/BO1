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


def dynamic(g, h, q, y_min, y_max, y_begining, y_end):
    # g - koszt produkcji ustalonej liczby produktów
    # h - koszt składowania
    # q - zapotrzebowania miesięczne na dany produkt
    # y_max/y_min - maksymalna/minimalna zajętość magazynu
    # y_begining/y_end - y na początku/końcu


    # inicjalizacja x jako macierz zer
    # f jako macierz funkcji celu
    # y - wektor dopuszczalnych ilości przedmiotów w magazynie
    x_matrix = np.zeros((y_max - y_min + 1, len(q)))
    f = np.full((y_max - y_min + 1, len(q)), np.inf)
    y = np.arange(y_min, y_max+1)

    # i, j to indeksy z macierzy wart. funkcji celu/ macierzy decyzji
    # nie należy ich odnosić od indeksowania z wykładu
    # i - kolejny wiersz w macierzy, czyli kolejny stan w danym etapie, czyli również
    # kolejna wart. f. celu oraz kolejna decyzja (kolejny x)
    # j - kolejna kolumna mazierzy, czyli kolejny etap procesu - kolejny miesiąc
    for j in range(f.shape[1]):
        for i in range(f.shape[0]):
            # indeksowanie dla macierzy wejściowych
            # czyli dla j = 0, input_index = etap końcowy
            input_index = f.shape[1] - j - 1

            # wyliczenie przedziału dopuszczalnej produkcji
            if j == 0:
                x_max = x_min = y_end + q[input_index] - y[i]
            else:
                x_min = max(y_min + q[input_index] - y[i], 0)
                x_max = min(y_max + q[input_index] - y[i], len(g)-1)

            # jeżeli warunki nie są spełnione przejdź do kolejnej iteracji
            if x_min > x_max or x_max < 0 or x_min < 0 or x_max > len(g)-1:
                x_matrix[i, j] = None
                f[i, j] = np.inf
                continue

            # sprawdzenie wszyskich możliwych ilości x
            for possible_x in range(x_min, x_max+1):
                # obliczenie kosztu
                if j != 0:
                    # - y_min, aby dostosować funkcję przejścia do indeksowania
                    cost = g[possible_x] + h[y[i] + possible_x - q[input_index] - y_min] + \
                           f[y[i] + possible_x - q[input_index] - y_min, j-1]
                else:
                    # cost = g[possible_x] + h[y[i] + possible_x - q[input_index]]
                    cost = g[possible_x]
                # sprawdzenie czy koszt jest mniejszy lub równy
                if cost < f[i, j]:
                    # uaktualnienie
                    x_matrix[i, j] = possible_x
                    f[i, j] = cost

    return x_matrix, f


def get_results(q, y_min, y_begining, x_matrix, f):
    state = y_begining
    strategy = f"Total cost = {f[y_begining - y_min, -1]}\n"

    for j in range(f.shape[1] - 1, -1, -1):
        input_index = f.shape[1] - j - 1
        decision = int(x_matrix[state - y_min, j])
        strategy += f"|y{input_index} = {state}, x{input_index} = {decision}|\n"
        state = int(state + decision - q[input_index])
    strategy += f"|y{len(q)} = {state}|\n"

    return strategy


g = np.array([0, 15, 18, 19, 20, 24])
h = np.array([i*2 for i in range(6)])
q = np.array([3,  3,  3,  3,  3,  3])
y_min = 0
y_max = 4
y_begining = 0
y_end = 0

ans = dynamic(g, h, q, y_min, y_max, y_begining, y_end)
print(f"X: \n{ans[0]} \n\nF: \n{ans[1]}\n")
print(get_results(q, y_min, y_begining, ans[0], ans[1]))

g = np.array([2, 8, 12, 15, 17, 20])
h = np.array([1, 2, 3, 4])
q = np.array([4, 2, 6, 5])
y_min = 2
y_max = 5
y_begining = 4
y_end = 3

ans = dynamic(g, h, q, y_min, y_max, y_begining, y_end)
print(f"X: \n{ans[0]} \n\nF: \n{ans[1]}\n")
print(get_results(q, y_min, y_begining, ans[0], ans[1]))

g = np.array([2, 8, 12, 15, 17, 20, 36, 40])
h = np.array([1, 2, 4, 8, 16, 32])
q = np.array([random.randint(0, 10) for i in range(12)])
y_min = 3
y_max = 7
y_begining = 5
y_end = 3

print(f"q: \n{q}")
ans = dynamic(g, h, q, y_min, y_max, y_begining, y_end)
print(f"X: \n{ans[0]} \n\nF: \n{ans[1]}\n")
print(get_results(q, y_min, y_begining, ans[0], ans[1]))