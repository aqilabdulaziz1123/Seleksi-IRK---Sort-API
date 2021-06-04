def list_to_html(l):
    table = '<table class="table table-bordered"><tbody>'

    l1 = list(range(0,len(l[0])))
    l2 = ["Column "+str(i) for i in l1]

    table += '<tr class="active"><td>'
    table += '</td><b></b><td>'.join(l2)
    table += '  </td></tr>'

    for sublist in l:
        table += '  <tr class="active"><td>'
        table += '    </td><td>'.join(sublist)
        table += '  </td></tr>'
    table += '</tbody></table>'

    return table

def list_to_string(list):
    result = '\n'.join(';'.join('%s' %x for x in y) for y in list)
    return result

def string_to_list(text):
    result = []
    rows = text.split('\\n')

    for row in rows:
        cols = row.split(';')
        temp = []
        
        for col in cols:
            temp += [col]

        result += [temp]

    return result