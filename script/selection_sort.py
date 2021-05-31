import csv, io, time

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def comparable(input, asc):
    if asc :
        return min(input)
    else :
        return max(input)

def selection(inputFile, idColumn, order):
    start = time.time()

    data = []
    column = []
    stream = io.StringIO(inputFile.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    for row in csv_input:
        data.append(row)
    asc = order=="ASC"

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

    # print(column)
    for i in range(0,len(data)-1):
        try:
            idx = column.index(comparable(column[i:],asc))
        except:
            print(column[i])
        column[idx], column[i] = column[i], column[idx]
        data[i+1], data[idx+1] = data[idx+1], data[i+1]
    
    end = time.time()
    return data, end-start

if __name__ == "__main__":
    print(selection("No,Test\r\n12,1\r\n3,2\r\n4,3\r\n5,4",0,"ASC"))