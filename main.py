import csv
from time import time
import pandas as pd

def csv_to_list(file_name):
     # Create a dataframe from csv
    df = pd.read_csv(file_name, delimiter=',')
    data = []
    data.append(df.columns.to_list())
    values = df.values.tolist()
    for val in values:
        data.append(val)
    # # User list comprehension to create a list of lists from Dataframe rows
    # list_of_rows = [list(row) for row in df.values]
    # # Insert Column names as first list in list of lists
    # list_of_rows.insert(0, df.columns.to_list())
    # # Print list of lists i.e. rows
    return data

# def csv_to_list(file_name):
#     file = open(file_name, "r")
#     csv_reader = csv.reader(file)
#     data = []
#     for row in csv_reader:
#         data.append(row)
#     return data 

def list_to_table(list):
    table = """<table class="table table-hover">\n"""
    header = list[0]
    table += """  <tr>\n"""
    for column in header:
        table += """   <th>{0}</th>\n""".format(str(column).strip())
    table += """  </tr>\n"""
    row_data = list[1:]
    for line in row_data:
        table += """  <tr>\n"""
        for column in line:
            table += """    <td>{0}</td>\n""".format(str(column).strip())
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
    for i in range(1,N-1):
        for j in range(1,N-i):
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
    for i in range(1, N):
        key = data[i]
        j = i-1
        if (orientation == "asc"):
            while j > 0 and key[col_idx] < data[j][col_idx]:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
        else:
            while j > 0 and key[col_idx] > data[j][col_idx]:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
    execution_time = time() - start_time     
    return data, execution_time

### DRIVER ###
# print(csv_to_list("tes.csv"))
# print(csv_to_list("100 Sales Records.csv"))
# A = [64, 25, 12, 22, 11]
# B = [[1,2,3],[4,6,9],[2,3,10]]
# print_matrix(B)
# ins = insertion_sort(B,0,"desc")[0]
# bub = bubble_sort(B,0,"desc")[0]
# sel = selection_sort(B,0,"desc")[0]
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