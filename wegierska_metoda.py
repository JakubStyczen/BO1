from typing import List
import numpy as np
from copy import deepcopy
from random import randint

REDUCTION = 0
SIZE = 0


class Matrix:
    def __init__(self, matrix: List[List[int]]):
        self.matrix = np.array(matrix)
        self.base_matrix = deepcopy(self.matrix)
        self.size = len(matrix)
        self.reduction = 0

    def reduce_and_get_sum(self):
        for row in range(self.size):
            min_value = min(self.matrix[row])
            self.reduction += min_value
            for col in range(self.size):
                self.matrix[row][col] -= min_value

    def reduce_matrix(self):
        # reduce rows and update reduction sum
        self.reduce_and_get_sum()
        # reduce cols and update reduction sum
        self.matrix = self.matrix.T
        self.reduce_and_get_sum()
        self.matrix = self.matrix.T
        return self.reduction

    def indep_zeros(self, start):
        rows_with_zero = []
        cols_with_zero = []
    

        for i, row in enumerate(self.matrix):
            for j, elem in enumerate(row):
                if elem == 0 and i not in rows_with_zero and j not in cols_with_zero:
                    rows_with_zero.append(i)
                    cols_with_zero.append(j)

        if start == len(rows_with_zero):
            rows_with_zero = []
            cols_with_zero = []
            for i, row in enumerate(self.matrix):
                if list(row).count(0) == 1:
                    rows_with_zero.append(i)
                    cols_with_zero.append(list(row).index(0))
            for i, row in enumerate(self.matrix):
                for j, elem in enumerate(row):
                    if elem == 0 and i not in rows_with_zero and j not in cols_with_zero:
                        rows_with_zero.append(i)
                        cols_with_zero.append(j)
        
        idxs_of_indep_zeros = [(i,j) for i, j in zip(rows_with_zero, cols_with_zero)]
        idxs_of_dep_zeros = []
        for i, row in enumerate(self.matrix):
            for j, elem in enumerate(row):
                if elem == 0 and (i,j) not in idxs_of_indep_zeros:
                    idxs_of_dep_zeros.append((i,j))
        return idxs_of_indep_zeros, idxs_of_dep_zeros

    def line_out(self, indep_zeros, dep_zeros):
        cols = set()
        rows = set()
        
        rows_indep_zeros = [zero[0] for zero in indep_zeros]
        start_len = -1
        while start_len != (len(cols) + len(rows)):
            start_len = len(cols) + len(rows)
            #1a rows without 0*
            for i in range(self.size):
                if i not in rows_indep_zeros:
                    rows.add(i)
            
            #1b cols with 0' in [rows]
            for row in rows:
                for zero in dep_zeros:
                    if zero[0] == row:
                        cols.add(zero[1])

            #1c
            for col in cols:
                for zero in indep_zeros:
                    if zero[1] == col:
                        rows.add(zero[0])
        
        #return rows to dash
        
            
        
        return [i for i in range(self.size) if i not in rows], list(cols)
         

    def min_lines(self):
        # DO POPRAWY poniższy kod  zadziała tylko w korzystnym przypadku, nie miałem lepszego pomysłu
        self.independent_row = []
        self.independent_col = []

        for row in range(self.size):
            for col in range(self.size):
                if (self.matrix[row][col] == 0) and (row not in self.independent_row) and (col not in self.independent_col):
                    if list(self.matrix[row]).count(0) > 1:
                        self.independent_row.append(row)
                        break
                    if list(self.matrix[:, col]).count(0) > 1:
                        self.independent_col.append(col)
                        break
                    self.independent_row.append(row)
                    break

    def create_additional_zeros(self):
        # znalezienie minimalnego elementu w niewykreślonej części
        min_element = np.inf
        for row in range(self.size):
            for col in range(self.size):
                if (row not in self.independent_row) and (col not in self.independent_col):
                    if self.matrix[row, col] < min_element:
                        min_element = self.matrix[row, col]

        # odjęcie minimalnego elementu od niewykreślonej części
        for row in range(self.size):
            for col in range(self.size):
                if (row not in self.independent_row) and (col not in self.independent_col):
                    self.matrix[row, col] -= min_element

                # dodanie do wszystkich przykrytych dwoma liniami
                elif (row in self.independent_row) and (col in self.independent_col):
                    self.matrix[row, col] += min_element

    # def get_total_cost(self):
    #     optimal_points = []
    #     total_cost = 0
    #
    #     chosen_col = []
    #     chosen_row = []
    #     for row in range(self.size):
    #         minimal_zeros = np.inf
    #         best_candidate = []
    #         for col in range(self.size):
    #             if (self.matrix[row, col] == 0) and (col not in chosen_col):
    #                 number_of_zeros = 0
    #                 # obliczenie liczby niewykreślonych zer w kolumnie
    #                 for col_row in range(self.size):
    #                     if (self.matrix[col_row, col] == 0) and (col_row not in chosen_row):
    #                         number_of_zeros += 1
    #                 if number_of_zeros < minimal_zeros:
    #                     minimal_zeros = number_of_zeros
    #                     best_candidate = [row, col]
    #
    #         optimal_points.append((best_candidate[0], best_candidate[1]))
    #         total_cost += self.base_matrix[best_candidate[0], best_candidate[1]]
    #         chosen_row.append(best_candidate[0])
    #         chosen_col.append(best_candidate[1])
    #
    #     return optimal_points, total_cost

    def get_total_cost(self):
        optimal_points = []
        total_cost = 0

        # uszeregownie kolejności wyboru wierszy
        # od tych z najmniejszą liczbą zero do tych
        # z największą
        rows = list()
        for i in range(self.size):
            for row in range(self.size):
                if list(self.matrix[row]).count(0) == i+1:
                    rows.append(row)

        chosen_col = []
        chosen_row = []
        for row in rows:
            minimal_zeros = np.inf
            best_candidate = []
            for col in range(self.size):
                if (self.matrix[row, col] == 0) and (col not in chosen_col):
                    number_of_zeros = 0
                    # obliczenie liczby niewykreślonych zer w kolumnie
                    for col_row in range(self.size):
                        if (self.matrix[col_row, col] == 0) and (col_row not in chosen_row):
                            number_of_zeros += 1
                    if number_of_zeros < minimal_zeros:
                        minimal_zeros = number_of_zeros
                        best_candidate = [row, col]

            optimal_points.append((best_candidate[0], best_candidate[1]))
            total_cost += self.base_matrix[best_candidate[0], best_candidate[1]]
            chosen_row.append(best_candidate[0])
            chosen_col.append(best_candidate[1])

        return optimal_points, total_cost

    def additional_zeros(self, rows, cols):
        #4a finding min elem
        min_elem = float('inf')
        for row in range(self.size):
            for col in range(self.size):
                if row not in rows and col not in cols:
                    if min_elem > self.matrix[row][col]:
                        min_elem = self.matrix[row][col]
                    
        #4b subtract it from all exisiting elems
        for row in range(self.size):
            for col in range(self.size):
                if row not in rows and col not in cols:
                    self.matrix[row][col] -= min_elem
                
                
        #4c add to double dashed elems
        for row in rows:
            for col in cols:
                self.matrix[row][col] += min_elem
        
        #4d inc reduction by min_elem
        self.reduction += min_elem

    def hunarian_algorithm(self):
        #1
        self.reduce_matrix()
        #2
        indep_zeros, dep_zeros = self.indep_zeros(0)
        while len(indep_zeros) != self.size:
            #3
            min_rows, min_cols = self.line_out(indep_zeros, dep_zeros)
            #4
            self.additional_zeros(min_rows, min_cols)
            indep_zeros, dep_zeros = self.indep_zeros(len(indep_zeros))

        #return Xij and value of func
        Xij = np.zeros((self.size, self.size))
        for pair in indep_zeros:
            Xij[pair[0]][pair[1]] = 1
        return Xij, self.reduction
        
        

    def hungarian_method(self):   # zwracanie wyniku końcowego jeśli liczba nizależnych zer jest równa rozmiarowi macierzy
        self.reduce_matrix()
        self.min_lines()
        print("\n\nMacierz pośrednia:\n", self.matrix)

        while True:
            if len(self.independent_col) + len(self.independent_row) == self.size:
                return self.get_total_cost()
            else:
                self.create_additional_zeros()
                self.min_lines()
                print("\n\nMacierz pośrednia:\n", self.matrix)




        
# to w celach testowych było, macierz jest z jego przykładu, można wywalić
if __name__ == '__main__':
    matrix = np.array([ #podawana macierz
        [6, 1, 5, 9, 2, 8],
        [7, 4, 9, 6, 9, 8],
        [9, 4, 9, 7, 1, 8],
        [0, 6, 5, 9, 7, 3],
        [4, 4, 4, 0, 1, 5],
        [7, 9, 3, 5, 8, 8]
    ])
    cp_matrix = deepcopy(matrix)
    
    # print('Macierz przed redukcją:\n', matrix_example.matrix)
    # print('\nSuma redukcji: ', matrix_example.reduce_matrix(), '\n')
    # print('Macierz po redukcji:\n', matrix_example.matrix)
    # a, b = matrix_example.indep_zeros()
    # r, c = matrix_example.line_out(a, b)
    # matrix_example.additional_zeros(r, c)
    # a, b = matrix_example.indep_zeros()
    # print(matrix_example.matrix)
    # print(matrix_example.reduction)
    
    print(matrix_example.hunarian_algorithm())
    
    
    # print(a, b)

    # matrix_example = Matrix([
    #     [82, 83, 69, 92],
    #     [77, 37, 49, 92],
    #     [11, 69, 5, 86],
    #     [8, 9, 98, 23]
    # ])
    #
    # matrix_example2 = Matrix([
    #     [20, 40, 10, 50],
    #     [100, 80, 30, 40],
    #     [10, 5, 60, 20],
    #     [70, 30, 10, 25]
    # ])
    #
    # print("Wynik", matrix_example.hungarian_method())
    # print("Wynik2", matrix_example2.hungarian_method())

    # matrix_example = Matrix([
    #     [5, 2, 3, 2, 7, 4, 10],
    #     [6, 8, 4, 2, 5, 72, 1],
    #     [6, 4, 3, 7, 2, 2, 3],
    #     [6, 9, 0, 4, 0, 3, 5],
    #     [4, 1, 2, 4, 0, 1, 1],
    #     [9, 2, 7, 3, 2, 10, 2],
    #     [12, 2, 3, 2, 3, 1, 9]
    # ])
    # print("Macierz początkowa: \n", matrix_example.base_matrix)
    # result = matrix_example.hungarian_method()
    # print("\n\nMacierz końcowa: \n", matrix_example.matrix)
    # print("\n\nWynik", result)
    #
    # matrix_example = Matrix([
    #     [5, 2, 3, 2, 7, 4, 10],
    #     [6, 8, 4, 1, 5, 72, 7],
    #     [6, 4, 3, 7, 2, 2, 3],
    #     [6, 9, 0, 4, 0, 3, 5],
    #     [4, 3, 2, 4, 0, 3, 8],
    #     [9, 2, 7, 3, 2, 10, 2],
    #     [12, 2, 3, 2, 3, 2, 9]
    # ])
    # print("Macierz początkowa: \n", matrix_example.base_matrix)
    # result = matrix_example.hungarian_method()
    # print("\n\nMacierz końcowa: \n", matrix_example.matrix)
    # print("\n\nWynik", result)

    # matrix_example = []
    # for i in range(7):
    #     matrix_example.append([])
    #     for j in range(7):
    #         matrix_example[i].append(randint(3, 15))
    #
    # matrix_example = Matrix(matrix_example)

    # matrix_example = Matrix([[4,  6,  6,  5, 10,  6,  7],
    #                          [7, 13, 10,  9, 15, 12, 14],
    #                          [7, 13, 13, 13,  9, 12, 11],
    #                          [0, 10,  6,  8,  5,  6, 12],
    #                          [7,  4,  8, 15, 13, 11,  5],
    #                          [3,  3,  4,  4,  4,  5, 10],
    #                          [15, 12, 15, 14, 10, 12,  5]])
    # print("Macierz początkowa: \n", matrix_example.base_matrix)
    # result = matrix_example.hungarian_method()
    # print("\n\nMacierz końcowa: \n", matrix_example.matrix)
    # print("\n\nWynik", result)







