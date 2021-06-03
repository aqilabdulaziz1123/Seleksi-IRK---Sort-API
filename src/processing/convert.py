def list_to_html(list):
    table = '<table class="table table-bordered"><tbody>'
    for sublist in list:
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