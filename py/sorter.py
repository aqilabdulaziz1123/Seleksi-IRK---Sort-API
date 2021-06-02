import csv
from time import time
from io import StringIO

skipfirst = True

def condition(a, b, order):
    if order=="ASC":
      return a>b
    else:
      return a<b

def printcsv(data):
  for row in data:
    for i, col in enumerate(row):
      print(col, end=" ")
      if i == len(row)-1:
        print()

def csvtostr(data, delimiter = ","):
  rows = []

  for row in data:
    rows.append(delimiter.join(row))
  
  string = "\r\n".join(rows)

  return string

def strtocsv(data, delimiter = ","):
    data = data.replace("\r", "")
    rows = data.split("\n")
    out = []

    for row in rows:
        out.append(row.split(delimiter))
    
    return out

def csvtoarray(name):
  data = []
  tes = open(name, "r")
  reader = csv.reader(tes)

  skip = not skipfirst
  for row in reader:
    if skip:
      skip = False
      continue
    data.append(row)

  tes.close()
  return data

def fstocsvtoarray(file):
    # file = filestorage
  data = []
  #tes = open(name, "r")
  tes = StringIO(file.read().decode("utf-8"))
  reader = csv.reader(tes)

  skip = not skipfirst
  for row in reader:
    if skip:
      skip = False
      continue
    data.append(row)

  return data

def csvtohtml(data):
    out = '<table style="width:100%">'
    for row in data:
        out += "<tr>"
        for col in row:
            out += "<th>"+col+"</th>"
        out += "</tr>"
    out += "</table>"
    return out

def selectionsort(arr, col, order = "ASC"):
  t = time()
  for i in range(len(arr)):
    if i == 0 and skipfirst:
      continue
    min = i
    for j in range(i+1, len(arr)):
      if condition(arr[min][col], arr[j][col], order):
        min = j
    arr[i], arr[min] = arr[min], arr[i]
  
  return arr, time()-t

def bubblesort(arr, col, order="ASC"):
    t = time()
    n = len(arr)
    
    if skipfirst:
      start = 1

    for i in range(start, n):
        for j in range(start, n-i):
            if condition(arr[j][col], arr[j+1][col], order):
                arr[j], arr[j+1] = arr[j+1], arr[j]
    
    return arr, time()-t

def insertionsort(arr, col, order = "ASC"):
  t = time()
  n = len(arr)
    
  if skipfirst:
    start = 1
  
  for i in range(start+1, n):
    key = arr[i][col]
    keyrow = arr[i]
    j = i-1
    while j >= start and condition(arr[j][col], key, order):
      arr[j+1] = arr[j]
      j -= 1
    arr[j+1] = keyrow
  
  return arr, time()-t


def listalgo(withfunc = False):
    return {
        "selection": selectionsort if withfunc else 1,
        "bubble": bubblesort if withfunc else 1,
        "insertion": insertionsort if withfunc else 1
    }

def preprocess(data, col):
  willremove = []
  skipheader = skipfirst

  for row in data:
    if skipheader:
      skipheader = False
      continue
    
    if isinstance(row[col], int):
      willremove.append(row)
  
  for victim in willremove:
    data.remove(victim)
  
  return data

def sort(csvfile, column, algorithm, order = "ASC"):
    algo = listalgo(True)
    array = fstocsvtoarray(csvfile)

    if len(array) == 0 or len(array[0]) == 0:
        return None, None, None, "Empty file"

    if column >= len(array[0]):
        return None, None, None, "Invalid column id"
    
    array = preprocess(array, column)

    arr, time = algo[algorithm](array, column, order)
    html = csvtohtml(arr)
    return arr, html, time, None
