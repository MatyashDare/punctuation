import re, os



#открываем файлы
def open_file(filename):
    with open(filename, encoding='utf-8') as f:
        text = f.read()
        t = text.split('@')
    return t

#чистим файлы
def file_to_list(filename):
    sentences = []
    for i in open_file(filename):
        i_1 = re.sub('(<.*?>)', '', i)
        i_2 = re.sub(r'\n', '', i_1)
        sentences.append(i_2)
    return sentences

#ищем ошибки
def find_errors(filename):
    errors = []
    re_find_b = [r"From [a-z].? (?:point of view|viewpoint|perspective).*", r"From [A-Z][a-z]+'s (?:point of view|viewpoint|perspective).*", \
                     r'To [a-z]{2,5} mind', r'For (?:example|instance).*', r'(?:However|Nevertheless|Consequently|To start with|Firstly| \
Secondly|Thirdly|Moreover|On the other hand|In other words|In short|Surprisingly| \
Unsurprisingly|Hopefully|Interestingly|Obviously|In conclusion|To conclude|To sum up| \
Thus|Of course).*']

    re_check_b = [r'From [a-z]{2,5} (?:point of view|viewpoint|perspective), ', r"From [A-Z][a-z]+'s (?:point of view|viewpoint|perspective), ", \
               r'To [a-z]{2,5} mind, ', r'For (?:example|instance), ', r'(?:However|Nevertheless|Consequently|To start with|Firstly| \
    Secondly|Thirdly|Moreover|On the other hand|In other words|In short|Surprisingly| \
    Unsurprisingly|Hopefully|Interestingly|Obviously|In conclusion|To conclude|To sum up| \
    Thus|Of course), ']

    re_find_m = [r"\w*? from [a-z]{2,5} (?:point of view|viewpoint|perspective).*", r'\w*? to [a-z]{2,5} mind.*', \
                 r'\w*? for (?:example|instance).*', r'(?:however|nevertheless|consequently|to start with|firstly| \
    secondly|thirdly|moreover|on the other hand|in other words|in short|surprisingly| \
    unsurprisingly|hopefully|interestingly|obviously|in conclusion|to conclude|to sum up| \
    thus|of course).*']
    re_check_m = [r'.*, from [a-z]{2,5} (?:point of view|viewpoint|perspective), ', r'.*, to [a-z]{2,5} mind, ',\
                  r'.*, for (?:example|instance), ',  r'(?:however|nevertheless|consequently|to start with|firstly| \
    secondly|thirdly|moreover|on the other hand|in other words|in short|surprisingly| \
    unsurprisingly|hopefully|interestingly|obviously|in conclusion|to conclude|to sum up| \
    thus|of course), ']
    re_trigger1 = [r'.* (?:—|-|:) from [a-z]{2,5} (?:point of view|viewpoint|perspective), ', r'.* (?:—|-|:) to [a-z]{2,5} mind, ', \
                   r'.* (?:—|-|:) for (?:example|instance), ', r'.* (?:—|-|:) (?:however|nevertheless|consequently|to start with|firstly| \
    secondly|thirdly|moreover|on the other hand|in other words|in short|surprisingly| \
    unsurprisingly|hopefully|interestingly|obviously|in conclusion|to conclude|to sum up| \
    thus|of course), ' ]
    re_trigger2 = [r'.*, from [a-z]{2,5} (?:point of view|viewpoint|perspective) (?:—|-|:|.)', r'.*, to [a-z]{2,5} mind (?:—|-|:|.) (?:—|-|:|.)',\
                   r'.*, for (?:example|instance) (?:—|-|:|.)', r'.*, (?:however|nevertheless|consequently|to start with|firstly| \
    secondly|thirdly|moreover|on the other hand|in other words|in short|surprisingly| \
    unsurprisingly|hopefully|interestingly|obviously|in conclusion|to conclude|to sum up| \
    thus|of course) (?:—|-|:|.)']
    for el in file_to_list(filename):
        for find in range(len(re_find_b)):
            b = re.findall(re_find_b[find], el)
            if b:
                wtf = re.findall(re_check_b[find], el)
                if len(wtf) == 0:
                    errors.append(el)
        for find in range(len(re_find_m)):
            m = re.findall(re_find_m[find], el)
            if m:
                wtf = re.findall(re_check_m[find], el)
                tr1 = re.findall(re_trigger1[find], el)
                tr2 = re.findall(re_trigger2[find], el)
                if len(wtf) == 0 and len(tr1) == 0 and len(tr2) == 0:
                    errors.append(el)
    return errors

def writeln(filename):
    workbook = xlsxwriter.Workbook('ex.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    errors = find_errors(filename)
    for error in errors:
        worksheet.write(row, col, error[0])
        worksheet.write(row, col + 1, error[1])
        worksheet.write(row, col + 2, error[2])
        row += 1
    workbook.close()


def main():
    filename = '/Users/alina/Downloads/KT_13_1.txt'
    writeln(filename)


if __name__ == '__main__':
    main()
