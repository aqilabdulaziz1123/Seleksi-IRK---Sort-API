# Change list of column to list of row
def col_to_row(col_list):
    list_of_colname = col_list[0]
    list_of_row = []
    for col in col_list[1:]:
        for i in range (len(col)):
            list_of_row.append([col[i] for col in col_list[1:]])
        break
    list_of_row.insert(0, list_of_colname)
    
    return list_of_row

# Change list to csv
def list_to_csv(list_of_row):
    csv_result = ''
    for row in list_of_row:
        str_col = [str(col) for col in row]
        csv_result += ','.join(str_col) + '\n'
    return csv_result

# Change csv to list
def csv_to_list(csv_data):
    all_elements = csv_data.split('\n')
    result = []
    for element in all_elements:
        if element.split(',') != ['']:
            result.append(element.split(','))
    return result

# Change string to binary
def str_to_bin(string):
    result = ''.join(format(ord(char), '08b') for char in string)

    return result

# Change binary to string
def bin_to_str(binary_values):
    ascii_string = ''

    for binary_value in binary_values:
        an_integer = int(binary_value, 2)
        ascii_character = chr(an_integer)
        ascii_string += ascii_character

    return ascii_string

# Split the string every nth number
def split_string(string, n):
    split_strings = [string[index : index + n] for index in range(0, len(string), n)]

    return split_strings
