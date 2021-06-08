from time import time

def selection_sort(arr, colnum, orientation = "asc"):
    start = time()
    for i in range(1, len(arr)):
        IMin = i
        for j in range(i+1, len(arr)):
            if orientation == "asc" :
                if(arr[IMin][colnum] > arr[j][colnum]):
                    IMin = j
            else:
                if(arr[IMin][colnum] < arr[j][colnum]):
                    IMin = j
        arr[i], arr[IMin] = arr[IMin], arr[i]
    exectime = time()-start
    return arr, exectime

def insertion_sort(arr, colnum , orientation = "asc"):
    start = time()
    n = len(arr)
    if n > 1:
        for i in range(2, len(arr)):
            temp = arr[i]
            j = i-1
            if orientation == "asc":
                while(temp[colnum] < arr[j][colnum] and j > 0):
                    arr[j+1] = arr[j]
                    j = j-1
                arr[j+1] = temp
            else:
                while(temp[colnum] > arr[j][colnum] and j > 0):
                    arr[j+1] = arr[j]
                    j = j-1
                arr[j+1] = temp
    exectime = time()-start
    return arr, exectime

def bubble_sort(arr, colnum , orientation = "asc"):
    start = time()
    n = len(arr)
    for i in range(1, n-1):
        for j in range(1, n-i):
            if orientation == "asc" :
                if arr[j][colnum] > arr[j+1][colnum]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
            else:
                if arr[j][colnum] < arr[j+1][colnum]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
    exectime = time()-start
    return arr, exectime