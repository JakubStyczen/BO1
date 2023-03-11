#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Marek Lechowicz


from typing import List
import numpy as np


class Matrix:
    def __init__(self, matrix: List[List[int]]):
        self.matrix = np.array(matrix)
        self.size = len(matrix)

    def reduce_and_get_sum(self):
        lower_bound = 0

        for row in range(self.size):
            min_value = min(self.matrix[row])
            lower_bound += min_value
            for col in range(self.size):
                self.matrix[row][col] -= min_value

        return lower_bound

    def reduce_matrix(self):
        lower_bound = 0

        # reduce rows and update reduction sum
        lower_bound += self.reduce_and_get_sum()

        # reduce cols and update reduction sum
        self.matrix = self.matrix.T
        lower_bound += self.reduce_and_get_sum()
        self.matrix = self.matrix.T

        return lower_bound





# to w celach testowych było, macierz jest z jego przykładu, można wywalić
if __name__ == '__main__':
    matrix_example = Matrix([
        [5, 2, 3, 2, 7],
        [6, 8, 4, 2, 5],
        [6, 4, 3, 7, 2],
        [6, 9, 0, 4, 0],
        [4, 1, 2, 4, 0]
    ])

    print('Macierz przed redukcją:\n', matrix_example.matrix)
    print('\nSuma redukcji: ', matrix_example.reduce_matrix(), '\n')
    print('Macierz po redukcji:\n', matrix_example.matrix)