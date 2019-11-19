import re, os

import pandas as pd
from os import listdir
from os.path import isfile, join

# открываем файлы
def open_file(filename):
    with open(filename, encoding='utf-8') as f:
        text = f.read()
        t = re.sub(r'\n', '', text)
        t = t.split('@')
    return t


def find_errors(filename):
    errors = []
    errors_sentences = []
    t = open_file(filename)
    for index in range(len(t)):
        sent_and_mark = re.split(r'(?<=[.!?…])> ', t[index])
        s_and_m = ' '.join(sent_and_mark)
        marking = re.findall(r'<.*>', s_and_m)
        sentence = re.sub('\n', '',re.split(r'<.*>', s_and_m)[0])
        q = ' '.join(marking)
        more_less = re.findall(r'\<(?:more|less) AV0\>\<\w* AJ0\>(?:<[^>]+\s...>){0,7}\<than CJS\>', q)
        adj_er = re.findall(r'\<.* AJC\>(?:<[^>]+\s...>){0,7}\<than CJS\>', q)
        adv_er = re.findall(r'\<.* ADV\>(?:<[^>]+\s...>){0,7}\<than CJS\>', q)
        if more_less:
            if re.findall(r'\<(?:more|less) AV0\>\<\w* AJ0\>(?:<[^>]+\s...>){0,7}\<, PUN\>\<than CJS\>', q):
                errors.append(q)
                errors_sentences.append(sentence)
        elif adj_er:
            if re.findall(r'\<.* AJC\>(?:<[^>]+\s...>){0,7}\<, PUN\>\<than CJS\>', q):
                errors.append(q)
                errors_sentences.append(sentence)
        else:
            if re.findall(r'\<.* AV0\>(?:<[^>]+\s...>){0,7}\<, PUN\>\<than CJS\>', q):
                errors.append(q)
                errors_sentences.append(sentence)
    return errors_sentences

def writeln(d, list_of_dicts, filename):
    errors = find_errors(d+'/'+filename)
    for error in errors:
        d = {}
        d['File'] = filename
        d['Error'] = error
        list_of_dicts.append(d)


def main():
    list_of_dicts = []
    directory =  '/Users/pikachu/Desktop/new'
    dirs = [x[0] for x in os.walk(directory)]
    for d in dirs:
        onlyfiles = [f for f in listdir(d) if isfile(join(d, f))]
        for filename in onlyfiles:
            if filename.endswith(".txt"):
                writeln(d, list_of_dicts, filename)
    df = pd.DataFrame(list_of_dicts)
    df.to_excel('/Users/pikachu/Desktop/ex_lab_punct_than.xlsx', index=False)


if __name__ == '__main__':
    main()
