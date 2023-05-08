from copy import deepcopy

def johnson(tasks):
    inf = float('inf')
    cp = deepcopy(tasks)
    output = [[None for _ in range(len(tasks[0]))] for _ in range(2)]
    start_idx = 0
    end_idx = len(tasks[0])-1
    min_elem = []
    min_idx = []
    
    while start_idx <= end_idx:
        for row_id, row in enumerate(cp):
            min_elem.append(min(row))
            min_idx.append(cp[row_id].index(min_elem[row_id]))
        if min_elem[0] < min_elem[1] or min_elem[0] == min_elem[1]:
            output[0][start_idx] = cp[0][min_idx[0]]
            output[1][start_idx] = cp[1][min_idx[0]]
            start_idx += 1
            cp[0][min_idx[0]] = inf
            cp[1][min_idx[0]] = inf
        elif min_elem[0] > min_elem[1] or min_elem[0] == min_elem[1]:
            output[0][end_idx] = cp[0][min_idx[1]]
            output[1][end_idx] = cp[1][min_idx[1]]
            end_idx -= 1
            cp[0][min_idx[1]] = inf
            cp[1][min_idx[1]] = inf

        min_elem = []
        min_idx = []
    return output

def ending_times(tasks):
    cp = deepcopy(tasks)
    for idx, elem in enumerate(cp[0][:-1]):
        cp[0][idx+1] += cp[0][idx]
        cp[1][idx] += cp[0][idx]
    cp[1][-1] += cp[0][-1]
    
    return cp

# tasks = [
#     [9, 6, 8, 7, 12, 3],
#     [7, 3, 5, 10, 4, 7]
# ]

tasks = [
    [9, 6, 8, 7, 12, 3, 14, 15, 4, 5],
    [7, 3, 5, 10, 4, 7, 11, 20, 5, 2]
]
print(f'Uszeregowanie początkowe:\n{tasks[0]}\n{tasks[1]}\n')
tasks_ordered = johnson(tasks)
print(f'Uszeregowanie końcowe:\n{tasks_ordered[0]}\n{tasks_ordered[1]}\n')
end_times = ending_times(tasks)
print(f'Czasy zakończeń:\n{end_times[0]}\n{end_times[1]}\n')