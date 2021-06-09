from collections import Counter

def data_cleaning(l):
    data_types = []
    for i in l:
        try:
            data_types.append(type(i))
        except IndexError:
            pass
    print(data_types)
    c = Counter(data_types)
    count_type = [(i, c[i] / len(data_types) * 100.0) for i in c.most_common()]
    most_common_type = count_type[0]
    result = []
    for i in l:
        if isinstance(i, most_common_type[0][0]):
            result.append(i)
    print(result)
