import math
import time


class Sort:
    @staticmethod
    def selection_sort(arr, column, order):
        print(arr[1][2])
        start = time.time()
        if(order == "ASC"):
            for i in range(1, len(arr)-1):
                idxMin = i
                for j in range(i + 1, len(arr)-1):
                    if(arr[j][column] < arr[idxMin][column]):
                        idxMin = j
                # swap
                if(i != idxMin):
                    tmp = arr[i]
                    arr[i] = arr[idxMin]
                    arr[idxMin] = tmp

        elif(order == "DESC"):
            for i in range(1, len(arr)-1):
                idxMax = i
                for j in range(i + 1, len(arr)-1):
                    if(arr[j][column] > arr[idxMax][column]):
                        idxMax = j
                # swap
                if(i != idxMax):
                    tmp = arr[i]
                    arr[i] = arr[idxMax]
                    arr[idxMax] = tmp
        end = time.time()
        print(end - start)
        return (end - start)

    @staticmethod
    def merge(arr, i, k, j, column, order):
        tmp = []
        p = i
        q = k + 1
        while(p <= k and q <= j):
            if(order == "ASC"):
                if(arr[p][column] <= arr[q][column]):
                    tmp.append(arr[p])
                    p += 1
                else:
                    tmp.append(arr[q])
                    q += 1
            elif(order == "DESC"):
                if(arr[p][column] >= arr[q][column]):
                    tmp.append(arr[p])
                    p += 1
                else:
                    tmp.append(arr[q])
                    q += 1

        while(p <= k):
            tmp.append(arr[p])
            p += 1

        while(q <= j):
            tmp.append(arr[q])
            q += 1

        for r in range(i, j + 1):
            arr[r] = tmp[r-i]

    @staticmethod
    def merge_s(arr, i, j, column, order):
        if(i < j):
            k = math.floor((i + j)/2)
            Sort.merge_s(arr, i, k, column, order)
            Sort.merge_s(arr, k + 1, j, column, order)
            Sort.merge(arr, i, k, j, column, order)

    @staticmethod
    def merge_sort(arr, column, order):
        start = time.time()
        Sort.merge_s(arr, 1, len(arr)-2, column, order)
        end = time.time()
        print(end - start)
        return (end - start)
