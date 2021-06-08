import csv
import pandas as pd

ALLOWED_EXTENSIONS = ['csv']

def filereader_tocsv(file):
    csvfile = file.read().decode('utf-8')
    csvlistformat = csvfile.split('\r\n')
    return csvlistformat

def fileformtoarr(file):
    df = pd.read_csv(file)
    arr = []
    arr.append(list(df.columns))
    value_list = df.values.tolist()
    for val in value_list:
        arr.append(val)
    processedlist = datapreprocess(arr)
    return processedlist

def filetoarr(file):
    lists = []
    for i in filereader_tocsv(file):
        arr = i.split(',')
        if arr != ['']:
            lists.append(arr)
    return lists

def filestringtoarr(filestring):
    csvlistformat = filestring.split('\r\n')
    lists = []
    for i in csvlistformat:
        arr = i.split(',')
        if arr != ['']:
            lists.append(arr)
    return lists

def arrtofilestring(arr):
    rowlist = []

    for row in arr:
        rowstring = ','.join([str(item) for item in row])
        rowlist.append(rowstring)
    
    filestring = '\r\n'.join(rowlist)
    return filestring

def list_to_html(lists):
    table = "<table>\n"

    header = lists[0]
    table += "  <tr>\n"
    for column in header:
        table += "    <th>{0}</th>\n".format(str(column).strip())
    table += "  </tr>\n"

    for line in lists[1:]:
        row = line
        table += "  <tr>\n"
        for column in row:
            table += "    <td>{0}</td>\n".format(str(column).strip())
        table += "  </tr>\n"

    table += "</table>"
    return table

def datapreprocess(lists):
    # get type list from first row
    firstrow = lists[1]
    typelist = []
    index_to_remove = []
    for col in firstrow:
        typelist.append(type(col))

    # search index to remove   
    for i in range(2, len(lists)):
        for j in range(len(typelist)):
            if not isinstance(lists[i][j], typelist[j]) and i not in index_to_remove:
                index_to_remove.append(i)
    
    # delete element from biggest index
    index_to_remove.reverse()
    for idx in index_to_remove:
        lists.pop(idx)

    return lists

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_columnnum(arr, colidx):
    return len(arr[0]) > colidx

# arr = [["abjad", "nomor", "nama"] ,["a", 11, "Dzaki"]]

# file = 'test/100 Sales Records.csv'

# datapreprocess(arr)
# print(isinstance(arr[1][1], type(arr[1][1])))
# print(isinstance(arr[1][1], type(arr[1][2])))

# sample = fileformtoarr(file)[1]
# print(sample)
# for item in sample:
#     print(type(item))