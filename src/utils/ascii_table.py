def create_table(row_data):
    header = [str(x) for x in range(len(row_data))]
    cols = len(row_data)
    divider = '+'
    lines = ['|', '|']
    for i in range(cols):
        pivot = len(header[i]) if len(header[i]) > len(row_data[i]) else len(row_data[i])
        pivot += 2
        divider += '-'*pivot + '+'
        if(len(header[i]) > len(row_data[i])):
            lines[0] += ' '+ header[i] + ' |'
            lines[1] += ' '*(pivot-len(row_data[i])-1)  + row_data[i] + ' ' + '|'
        else:
            lines[0] += ' '*(pivot-len(header[i])-1) + header[i] + ' ' + '|'
            lines[1] += ' ' + row_data[i] + ' |'

    return '''{0}\n{1}\n{0}\n{2}\n{0}'''.format(divider, lines[0], lines[1])