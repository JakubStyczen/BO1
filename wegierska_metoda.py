from typing import List
import numpy as np
from copy import deepcopy
from random import randint


SIZE = 0

def reduce_and_get_sum(matrix):
    fi = 0
    SIZE = len(matrix)
    for row in range(SIZE):
        min_value = min(matrix[row])
        fi += min_value
        for col in range(SIZE):
            matrix[row][col] -= min_value
    return fi

def reduce_matrix(matrix):
    fi = 0
    # reduce rows and update reduction sum
    fi += reduce_and_get_sum(matrix)
    # reduce cols and update reduction sum
    matrix = matrix.T
    fi += reduce_and_get_sum(matrix)
    matrix = matrix.T
    return fi

def indep_zeros_search(start, matrix):
    rows_with_zero = []
    cols_with_zero = []


    for i, row in enumerate(matrix):
        for j, elem in enumerate(row):
            if elem == 0 and i not in rows_with_zero and j not in cols_with_zero:
                rows_with_zero.append(i)
                cols_with_zero.append(j)

    if start == len(rows_with_zero):
        rows_with_zero = []
        cols_with_zero = []
        for i, row in enumerate(matrix):
            if list(row).count(0) == 1:
                rows_with_zero.append(i)
                cols_with_zero.append(list(row).index(0))
        for i, row in enumerate(matrix):
            for j, elem in enumerate(row):
                if elem == 0 and i not in rows_with_zero and j not in cols_with_zero:
                    rows_with_zero.append(i)
                    cols_with_zero.append(j)
    
    idxs_of_indep_zeros = [(i,j) for i, j in zip(rows_with_zero, cols_with_zero)]
    idxs_of_dep_zeros = []
    for i, row in enumerate(matrix):
        for j, elem in enumerate(row):
            if elem == 0 and (i,j) not in idxs_of_indep_zeros:
                idxs_of_dep_zeros.append((i,j))
    return idxs_of_indep_zeros, idxs_of_dep_zeros



def line_out(indep_zeros, dep_zeros, matrix):
    cols = set()
    rows = set()
    SIZE = len(matrix)
    
    rows_indep_zeros = [zero[0] for zero in indep_zeros]
    start_len = -1
    while start_len != (len(cols) + len(rows)):
        start_len = len(cols) + len(rows)
        #1a rows without 0*
        for i in range(SIZE):
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
    return [i for i in range(SIZE) if i not in rows], list(cols)
        

def additional_zeros(rows, cols, matrix):
    SIZE = len(matrix)
    #4a finding min elem
    min_elem = float('inf')
    for row in range(SIZE):
        for col in range(SIZE):
            if row not in rows and col not in cols:
                if min_elem > matrix[row][col]:
                    min_elem = matrix[row][col]
                
    #4b subtract it from all exisiting elems
    for row in range(SIZE):
        for col in range(SIZE):
            if row not in rows and col not in cols:
                matrix[row][col] -= min_elem
            
            
    #4c add to double dashed elems
    for row in rows:
        for col in cols:
            matrix[row][col] += min_elem
    
    #4d inc reduction by min_elem
    return min_elem

def hunarian_algorithm(matrix):
    REDUCTION = 0
    SIZE = len(matrix)
    #1
    print(f'Macierz początkowa: \n{matrix}\n Ograniczenie dolne: {REDUCTION}\n')
    REDUCTION += reduce_matrix(matrix)
    print(f'Macierz po redukcji: \n{matrix}\n Ograniczenie dolne: {REDUCTION}\n')
    #2
    indep_zeros, dep_zeros = indep_zeros_search(0, matrix)
    while len(indep_zeros) != SIZE:
        #3
        min_rows, min_cols = line_out(indep_zeros, dep_zeros, matrix)
        #4
        REDUCTION += additional_zeros(min_rows, min_cols, matrix)
        print(f'Macierz po dodaniu zer: \n{matrix}\n Ograniczenie dolne: {REDUCTION}\n')
        indep_zeros, dep_zeros = indep_zeros_search(len(indep_zeros), matrix)
    #return Xij and value of func
    Xij = np.zeros((SIZE, SIZE))
    res = "Finalny wynik:\n"
    for pair in indep_zeros:
        Xij[pair[0]][pair[1]] = 1
        res += f'Pracownik {pair[1]+1} wykonuje zadanie {pair[0]+1}\n'
    res += f'Całkowity koszt: {REDUCTION}/n'
    print(res)
    return Xij, REDUCTION



    
        
if __name__ == '__main__':
    matrix = np.array([ 
        [6, 1, 5, 9, 2, 8],
        [7, 4, 9, 6, 9, 8],
        [9, 4, 9, 7, 1, 8],
        [0, 6, 5, 9, 7, 3],
        [4, 4, 4, 0, 1, 5],
        [7, 9, 3, 5, 8, 8]
    ])
    cp_matrix = deepcopy(matrix)
    
    
    hunarian_algorithm(matrix)
    


