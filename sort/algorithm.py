import copy
from flask.json import jsonify
from sort.database import *
from datetime import datetime

def selection_sort(jsonArray, idx, order):
    start = datetime.now()
    min_idx = 0
    tmpArray={}
    for i in range(len(jsonArray)-1):
        min_idx = i;
        for j in range(i+1,len(jsonArray)):
            list1=list(jsonArray[min_idx].values())
            list2=list(jsonArray[j].values())
            if (order=="asc"):
                if (list1[idx]>list2[idx]):
                    min_idx=j
            else:
                if (list1[idx]<list2[idx]):
                    min_idx=j
        tmpArray.update(jsonArray[min_idx])
        jsonArray[min_idx].update(jsonArray[i])
        jsonArray[i].update(tmpArray)
    duration = (datetime.now()-start).total_seconds()
    add_to_database(start, "selection", str(jsonArray), duration)
    return jsonArray


def bubble_sort(jsonArray, idx, order):
    start = datetime.now()
    tmpArray={}
    for i in range(len(jsonArray)-1):
        for j in range(len(jsonArray)-i-1):
            list1=list(jsonArray[j].values())
            list2=list(jsonArray[j+1].values())
            if (order=="asc"):
                if (list1[idx]>list2[idx]):
                    tmpArray.update(jsonArray[j])
                    jsonArray[j].update(jsonArray[j+1])
                    jsonArray[j+1].update(tmpArray)
            else:
                if (list1[idx]<list2[idx]):
                    tmpArray.update(jsonArray[j])
                    jsonArray[j].update(jsonArray[j+1])
                    jsonArray[j+1].update(tmpArray)                
    duration = (datetime.now()-start).total_seconds()
    add_to_database(start, "bubble", str(jsonArray), duration)
    return jsonArray


def insertion_sort(jsonArray, idx, order):
    start = datetime.now()
    tmpArray={}
    for i in range(1, len(jsonArray)):

        j=i-1
        list1 = list(jsonArray[i].values())
        list2 = list(jsonArray[j].values())
        tmpArray.update(jsonArray[j+1])
        if (order=="asc"):
            while j >= 0 and list1[idx]<list2[idx]:
                jsonArray[j+1].update(jsonArray[j])
                j-=1
        else:
            while j >= 0 and list1[idx]>list2[idx]:
                jsonArray[j+1].update(jsonArray[j])
                j-=1
        jsonArray[j+1].update(tmpArray)  
    duration = (datetime.now()-start).total_seconds()
    add_to_database(start, "bubble", str(jsonArray), duration)
    return jsonArray


def merge(jsonArray, idx, order):
    if (len(jsonArray))>1:
        mid = len(jsonArray) // 2
        left = copy.deepcopy(jsonArray[:mid])
        right = copy.deepcopy(jsonArray[mid:])

        merge(left, idx, order)
        merge(right,idx, order)

        i = 0
        j = 0
        k = 0

        while i < len(left) and j < len(right):
            listleft = list(left[i].values())
            listright = list(right[j].values())
            if (order == "asc"):
                if (listleft[idx]<listright[idx]):
                    jsonArray[k].update(left[i])
                    i+=1
                else:
                    jsonArray[k].update(right[j])
                    j+=1
            else:
                if (listleft[idx]<listright[idx]):
                    jsonArray[k].update(right[j])
                    j+=1
                else:
                    jsonArray[k].update(left[i])
                    i+=1
            k += 1
        
        while i < len(left):
            jsonArray[k].update(left[i])
            i +=1
            k +=1

        while j < len(right):
            jsonArray[k].update(right[j])
            j +=1
            k +=1
    return jsonArray
def merge_sort(jsonArray, idx, order):
    start = datetime.now()
    jsonArray = merge(jsonArray, idx, order)
    duration = (datetime.now()-start).total_seconds()
    add_to_database(start, "bubble", str(jsonArray), duration)
    return jsonArray

def partition(jsonArray, idx, order, low, high):
    tmpArray={}
    i = low -1
    pivot = list(jsonArray[high].values())

    for j in range(low, high):
        list1 = list(jsonArray[j].values())
        if (order=="asc"):
            if (list1[idx]<=pivot[idx]):
                i = i+1
                tmpArray.update(jsonArray[j])
                jsonArray[j].update(jsonArray[i])
                jsonArray[i].update(tmpArray)
        else:
            if (list1[idx]>=pivot[idx]):
                i = i+1
                tmpArray.update(jsonArray[j])
                jsonArray[j].update(jsonArray[i])
                jsonArray[i].update(tmpArray) 
    tmpArray.update(jsonArray[high])
    jsonArray[high].update(jsonArray[i+1])
    jsonArray[i+1].update(tmpArray)
    return i+1         



def quick(jsonArray, idx, order, low, high):
    if len(jsonArray) == 1:
        return jsonArray
    if low < high:
  
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(jsonArray, idx, order, low, high)
  
        # Separately sort elements before
        # partition and after partition
        quick(jsonArray, idx, order, low, pi-1)
        quick(jsonArray, idx, order, pi+1, high)


def quick_sort(jsonArray, idx, order):
    start = datetime.now()
    quick(jsonArray, idx, order, 0 , len(jsonArray)-1)
    duration = (datetime.now()-start).total_seconds()
    add_to_database(start, "bubble", str(jsonArray), duration)
    return jsonArray