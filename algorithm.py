import json
import time
from database import insertData

def selectionsort (jsonArray, columnIdx, orientation):
    start_time = time.time()
    keys = list(jsonArray[0].keys())
    key = keys[columnIdx]
    for i in range (len(jsonArray)):
        min_idx = i
        for j in range (i+1, len(jsonArray)):
            if(orientation == "asc"):
                try:
                    if (float(jsonArray[min_idx][key]) > float(jsonArray[j][key])):
                        min_idx = j
                except ValueError:
                    if (jsonArray[min_idx][key] > jsonArray[j][key]):
                        min_idx = j
            elif (orientation == 'desc'):
                try:
                    if (float(jsonArray[min_idx][key]) < float(jsonArray[j][key])):
                        min_idx = j
                except ValueError:
                    if (jsonArray[min_idx][key] < jsonArray[j][key]):
                        min_idx = j
                
        # Swap the found minimum element with
        # the first element       
        jsonArray[i], jsonArray[min_idx] = jsonArray[min_idx], jsonArray[i]
    end_time = time.time()
    exectime = end_time - start_time # in seconds
    return jsonArray, exectime

def bubbleSort(jsonArray, columnIdx, orientation):
    start_time = time.time()
    keys = list(jsonArray[0].keys())
    key = keys[columnIdx]
    n = len(jsonArray)
  
    # Traverse through all array elements
    for i in range(n-1):
    # range(n) also work but outer loop will repeat one time more than needed.
  
        # Last i elements are already in place
        for j in range(0, n-i-1):
  
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if (orientation == 'asc'):
                try:
                    if float(jsonArray[j][key]) > float(jsonArray[j + 1][key]) :
                        jsonArray[j], jsonArray[j + 1] = jsonArray[j + 1], jsonArray[j]
                except ValueError:
                    if jsonArray[j][key] > jsonArray[j + 1][key]:
                        jsonArray[j], jsonArray[j + 1] = jsonArray[j + 1], jsonArray[j]
            else:
                try:
                    if float(jsonArray[j][key]) < float(jsonArray[j + 1][key]) :
                        jsonArray[j], jsonArray[j + 1] = jsonArray[j + 1], jsonArray[j]
                except ValueError:
                    if jsonArray[j][key] < jsonArray[j + 1][key]:
                        jsonArray[j], jsonArray[j + 1] = jsonArray[j + 1], jsonArray[j]
    end_time = time.time()
    exectime = end_time - start_time # in seconds
    return jsonArray, exectime