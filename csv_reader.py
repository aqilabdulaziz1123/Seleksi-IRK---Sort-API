import pandas as pd
import csv

# Read a csv file and get a column in it
def column_csv_reader(filename, column_no):
    with open(filename) as csv_file:
        # Use ',' delimiter for csv
        reader = csv.reader(csv_file, delimiter=',')
        column_name = ''
        list_of_row = []
        i = 0
        for row in reader:
            try:
                # Column name must be on the first row
                if i == 0:
                    column_name += row[column_no-1]
                    i += 1

                # List of tuples
                else:
                    list_of_row.append(row[column_no-1].strip())
                    i += 1
            except IndexError:
                pass
    
    return column_name, list_of_row
