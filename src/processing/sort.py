import csv
import time

def selection_sort(data, col, orient):
    start_time = time.time()

    for i in range(len(data)):
        idx = i

        for j in range(i+1, len(data)):
            if (orient == "ASC"):
                if (data[idx][col] > data[j][col]):
                    idx = j
            elif (orient == "DESC"): 
                if (data[idx][col] < data[j][col]):
                    idx = j  

        data[i], data[idx] = data[idx], data[i]

    exec_time = time.time() - start_time

    return data, exec_time

def bubble_sort(data, col, orient):
    start_time = time.time()

    for i in range(len(data)-1,0,-1):
        for j in range(i):
            if (orient == "ASC"):
                if data[j][col] > data[j+1][col]:
                    temp = data[j]
                    data[j] = data[j+1]
                    data[j+1] = temp
            elif (orient == "DESC"):
                if data[j][col] < data[j+1][col]:
                    temp = data[j]
                    data[j] = data[j+1]
                    data[j+1] = temp                

    exec_time = time.time() - start_time

    return data, exec_time

def insertion_sort(data, col, orient):
    start_time = time.time()

    for i in range(1, len(data)):
        j = i-1
        nxt_element = data[i]
		
        if (orient == "ASC"):
            while (data[j][col] > nxt_element[col]) and (j >= 0):
                data[j+1] = data[j]
                j=j-1
        elif (orient == "DESC"): 
            while (data[j][col] < nxt_element[col]) and (j >= 0):
                data[j+1] = data[j]
                j=j-1

        data[j+1] = nxt_element

    exec_time = time.time() - start_time

    return data, exec_time

def merge_sort(data, col, orient):
    start_time = time.time()

    if len(data) > 1:
 
        # Finding the mid of the dataay
        mid = len(data)//2
 
        # Dividing the data elements into two
        L = data[:mid]
        R = data[mid:]
 
        # Sorting the first and second half
        left_sorted, exec = merge_sort(L, col, orient)
        right_sorted, exec = merge_sort(R, col, orient)
 
        i = j = k = 0
 
        # Copy data to temp dataays L[] and R[]
        while i < len(left_sorted) and j < len(right_sorted):
            if (orient == "ASC"):
                if left_sorted[i][col] < right_sorted[j][col]:
                    data[k] = left_sorted[i]
                    i += 1
                else:
                    data[k] = right_sorted[j]
                    j += 1
                k += 1
            elif (orient == "DESC"): 
                if left_sorted[i][col] > right_sorted[j][col]:
                    data[k] = left_sorted[i]
                    i += 1
                else:
                    data[k] = right_sorted[j]
                    j += 1
                k += 1
 
        # Checking if any element was left
        while i < len(left_sorted):
            data[k] = left_sorted[i]
            i += 1
            k += 1
 
        while j < len(right_sorted):
            data[k] = right_sorted[j]
            j += 1
            k += 1

    exec_time = time.time() - start_time

    return data, exec_time