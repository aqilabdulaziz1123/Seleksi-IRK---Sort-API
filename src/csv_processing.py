import re
import pandas as pd
from collections import Counter

def clean_strip(filename):
    cleaned_filename = re.search('(.*)\.csv', filename).group(1)
    with open(filename, 'r', newline='') as inf, open(f'{cleaned_filename}_cleaned.csv', 'w') as of:
        for line in inf:
            trimmed = (field.strip().strip('"') for field in line.split(','))
            of.write(','.join(trimmed)+'\n')

def data_preprocess(filename):
    cleaned_filename = re.search('(.*)\.csv', filename).group(1)
    df = pd.read_csv(f'{cleaned_filename}_cleaned.csv')
    to_be_parsed = []
    list_of_colname = df.columns.tolist()
    to_be_parsed.append(list_of_colname)
    for value in df.values.tolist():
        to_be_parsed.append(value)
    list_of_column = []
    data_types = []
    for row in to_be_parsed[1:]:
        for i in range (len(row)):
            list_of_column.append([row[i] for row in to_be_parsed[1:]])
            data_types.append([type(row[i]) for row in to_be_parsed[1:]])
        break
    i = 0
    result = []
    for data_type in data_types:
        c = Counter(data_type)
        count_type = [(i, c[i] / len(data_types) * 100.0) for i in c.most_common()]
        most_common_type = count_type[0]
        result.append([col for col in list_of_column[i] if isinstance(col, most_common_type[0][0])])
        i += 1
    result.insert(0, list_of_colname)

    return result
