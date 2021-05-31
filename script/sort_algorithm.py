import csv, io, time

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def configureInput(inputFile, idColumn):
    data = []
    column = []
    stream = io.StringIO(inputFile.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    for row in csv_input:
        data.append(row)

    first = True
    second = True
    intType = True
    removedRow = []
    for row in data:
        if first:
            first = False
            continue
        elif not first and second:
            intType = is_int(row[idColumn])
            second = False

        if intType ^ is_int(row[idColumn]):
            removedRow.append(row)
            continue

        column.append(int(row[idColumn]) if intType else row[idColumn].lower())

    for row in removedRow:
        data.remove(row)
    
    return data, column

def selection(inputFile, idColumn, order):
    def comparable(input, asc):
        if asc :
            return min(input)
        else :
            return max(input)

    start = time.time()
    asc = order=="ASC"

    data, column = configureInput(inputFile, idColumn)
    print(len(column),len(data))
    
    for i in range(0,len(data)-1):
        idx = column[i:].index(comparable(column[i:],asc)) + i
        column[idx], column[i] = column[i], column[idx]
        data[i+1], data[idx+1] = data[idx+1], data[i+1]
    
    end = time.time()
    return data, end-start

def insertion(inputFile, idColumn, order):
    comparable = lambda a,b : (a<b if order=="ASC" else a>b)
    start = time.time()

    data, column = configureInput(inputFile, idColumn)

    # print(column)
    print(len(column),len(data))
    for i in range(1,len(data)):
        key = column[i-1]
        val = data[i]

        j = i-1
        while j>0 and comparable(key,column[j-1]):
            column[j] = column[j-1]
            data[j+1] = data[j]
            j -= 1
        
        column[j] = key
        data[j+1] = val

    # print(data)
    end = time.time()
    return data, end-start

def bubble(inputFile, idColumn, order):
    comparable = lambda a,b : (a<b if order=="ASC" else a>b)

    start = time.time()

    data, column = configureInput(inputFile, idColumn)

    # print(column)
    n = len(data)
    for i in range(1,n):
        for j in range(1, n-i):
            if not comparable(column[j-1],column[j]) :
                column[j], column[j-1] = column[j-1], column[j]
                data[j], data[j+1] = data[j+1], data[j]
    
    end = time.time()
    return data, end-start

if __name__ == "__main__":
    print(selection("No,Test\r\n12,1\r\n3,2\r\n4,3\r\n5,4",0,"ASC"))