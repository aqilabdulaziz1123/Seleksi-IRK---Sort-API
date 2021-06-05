import csv

# Read a csv file and get a column in it
def column_csv_reader(filename, column_no):
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        list_of_row = []
        for row in reader:
            list_of_row.append(row[column_no+1])
    return list_of_row
