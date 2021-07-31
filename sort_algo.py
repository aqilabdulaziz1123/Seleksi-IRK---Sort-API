import time
from datetime import datetime

def type_check(unsorted_matrix, relative_col_idx, asc):
    if (type(unsorted_matrix) is list and type(relative_col_idx) is int and type(asc) is bool):
        return True
    return False

def selection_sort(unsorted_matrix, relative_col_idx, asc):
    retval = {
        "tanggal_waktu" : datetime.now(),
        "sorted_matrix" : [],
        "delta_time" : 0.0
    }
    # type check
    if type_check(unsorted_matrix, relative_col_idx, asc) == False:
        return retval
    
    # col_idx check
    if relative_col_idx < 0 or relative_col_idx >= len(unsorted_matrix):
        return retval

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
        
        # swap
        unsorted_matrix[current_idx], unsorted_matrix[min_value_idx] = unsorted_matrix[min_value_idx], unsorted_matrix[current_idx]
        # append to sorted matrix
        sorted_matrix.append(unsorted_matrix[current_idx])
        current_idx += 1
    # end sorting
    time_end = time.time()
    # END

    delta_time = time_end-time_start
    retval["sorted_matrix"] = sorted_matrix
    retval["delta_time"] = delta_time

    return retval




    