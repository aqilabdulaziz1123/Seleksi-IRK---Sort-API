import time
from sort_algo import selection_sort
usa = [2,46,32,1,43,33,26,84,26,62,100,40,77,50,67,97,60,18,69,59]
sa = []
for num in usa:
    sa.append(num)
sa.sort()

def sel_sort(unsorted_matrix, relative_col_idx, asc):
    retval = {
        "sorted_matrix" : [],
        "delta_time" : 0.0
    }
    sorted_matrix = []
    
    # algo_components
    current_idx = 0
    min_value_idx = 0
    max_idx = len(unsorted_matrix) - 1

    # START
    time_start = time.time()

    # sorting
    while current_idx <= max_idx:
        min_value_idx = current_idx
        # getting min_value_idx
        for i in range (current_idx, max_idx+1):
            if asc:
                if unsorted_matrix[i][relative_col_idx] < unsorted_matrix[min_value_idx][relative_col_idx]:
                    min_value_idx = i
            else:
                if unsorted_matrix[i][relative_col_idx] > unsorted_matrix[min_value_idx][relative_col_idx]:
                    min_value_idx = i
        unsorted_matrix[current_idx], unsorted_matrix[min_value_idx] = unsorted_matrix[min_value_idx], unsorted_matrix[current_idx]
        sorted_matrix.append(unsorted_matrix[current_idx])
        # print(sorted_matrix)
        current_idx += 1
    # end sorting
    time_end = time.time()
    # END

    delta_time = time_end-time_start
    retval["sorted_matrix"] = sorted_matrix
    retval["delta_time"] = delta_time

    return retval

print(usa)
print(sa)
matrix = [
    [17,2,86,5,71],
    [95,46,69,56,31],
    [63,32,58,4,79],
    [14,1,38,50,23],
    [9,43,7,80,76],
    [2,33,40,66,35],
    [73,26,42,93,40],
    [85,84,44,64,62],
    [37,26,39,85,15],
    [79,62,41,90,72],
    [98,100,56,33,41],
    [26,40,89,37,41],
    [94,77,82,56,86],
    [72,50,10,38,31],
    [47,67,94,39,81],
    [65,97,43,34,9],
    [17,60,10,16,2],
    [72,18,42,12,50],
    [58,69,79,61,62],
    [94,59,77,29,13]
]
# for row in matrix[:5]:
#     print(row)
sm = sel_sort(matrix, 0, True)["sorted_matrix"]
for row in sm:
    print(row)

print("0=[=====- X -=====]=0")
sm2 = selection_sort(matrix, 0, True)["sorted_matrix"]
for row in sm2:
    print(row)