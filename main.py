import csv
from time import time

def csv_to_list(file_name):
    file = open(file_name, "r")
    csv_reader = csv.reader(file)
    data = []
    for row in csv_reader:
        data.append(row)
    return data 

# def string_to_csv(file_name, string):
#     file = open(file_name, "w")
#     csv_writer = csv.writer(file)
#     csv_writer.writerow(string)

def list_to_table(list):
    table = """<table>\n"""
    # Create the table's column headers
    header = list[0]
    table += """  <tr>\n"""
    for column in header:
        table += """   <th>{0}</th>\n""".format(column.strip())
    table += """  </tr>\n"""
    # Create the table's row data
    row_data = list[1:]
    for line in row_data:
        table += """  <tr>\n"""
        for column in line:
            table += """    <td>{0}</td>\n""".format(column.strip())
        table += """  </tr>\n"""
    table += """</table>"""
    return table

def list_to_string(data):
    string = ""
    for i in range(len(data)):
        for j in range(len(data[0])):
            if (j != (len(data[0])-1)):
                string += str(data[i][j]) + ","
            else:
                string += str(data[i][j])
        if (i != (len(data)-1)):
            string += '\n'
    return string

def string_to_list(input_string):
    result = []
    string = input_string.decode('UTF-8')
    rows = string.split('\n')
    for row in rows:
        cols = row.split(',')
        cols_list = []
        for col in cols:
            cols_list.append(col)
        result.append(cols_list)
    return result

def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(matrix[i][j],end=" ")
        print()

def selection_sort(data, col_idx, orientation):
    start_time = time()
    N = len(data)
    for i in range(1,N):
        min_idx = i
        for j in range(i+1,N):
            if (orientation == "asc"):
                if data[min_idx][col_idx] > data[j][col_idx]:
                    min_idx = j
            else:
                if data[min_idx][col_idx] < data[j][col_idx]:
                    min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]   
    execution_time = time() - start_time     
    return data, execution_time

def bubble_sort(data, col_idx, orientation):
    start_time = time()
    N = len(data)
    # Traverse through all array elements
    for i in range(1,N):
        # Last i elements are already in place
        for j in range(0, N-i-1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if (orientation == "asc"):
                if data[j][col_idx] > data[j+1][col_idx]:
                    data[j], data[j+1] = data[j+1], data[j]
            else: 
                if data[j][col_idx] < data[j+1][col_idx]:
                    data[j], data[j+1] = data[j+1], data[j]
    execution_time = time() - start_time     
    return data, execution_time

def insertion_sort(data, col_idx, orientation):
    start_time = time()
    N = len(data)
    # Traverse through 1 to len(arr)
    for i in range(2, N):
        key = data[i]
        # Move elements of data[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i-1
        if (orientation == "asc"):
            while j >= 0 and key[col_idx] < data[j][col_idx]:
                    data[j + 1] = data[j]
                    j -= 1
        else:
            while j >= 0 and key[col_idx] > data[j][col_idx]:
                    data[j + 1] = data[j]
                    j -= 1
        data[j + 1] = key
    execution_time = time() - start_time     
    return data, execution_time

A = [64, 25, 12, 22, 11]
B = [[1,2,3],[4,6,9],[2,3,10]]
print_matrix(B)
ins = insertion_sort(B,0,"desc")[0]
bub = bubble_sort(B,0,"desc")[0]
sel = selection_sort(B,0,"desc")[0]
# print("Insertion sort")
# print_matrix(ins)
# print("Bubble sort")
# print_matrix(bub)
# print("Selection sort")
# print_matrix(sel)
# print("CSV")
# list_tes = csv_to_list("tes.csv")
# html_tes = list_to_table(list_tes)
# string_tes = list_to_string(list_tes)
# print(list_tes)
# print(html_tes)
# print(string_tes)
# # string_to_csv("haites.csv",string_tes)
# list_daristring = string_to_list(string_tes)
# print(list_daristring)