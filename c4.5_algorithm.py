import csv
import math
from collections import OrderedDict, defaultdict

# csv file name
csv_file_name = 'test.csv'

csv_table = {}


def create_table():
    # считываем данные из csv файла
    with open(csv_file_name, "r") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        for row in reader:
            for pair in row.items():
                if csv_table.get(pair[0]) is None:
                    csv_table.update({pair[0]: []})

                dict_list = list(csv_table.get(pair[0]))
                dict_list.insert(len(dict_list), pair[1])

                csv_table.update({pair[0]: dict_list})


# считаем кол-во примеров для заданного атрибута из таблицы
def freq(table, column, value):
    return table[column].count(value)


# получаем список, который содержит уникальные примеры для атрибута
def delete_duplications(li):
    return OrderedDict.fromkeys(li)


# получаем новую таблицу, примеры атрибутов которых удовлетворяют индексам
def del_values(table, indexes):
    return {k: [v[i] for i in range(len(v)) if i in indexes] for k, v in table.items()}


# получаем список индексов заданного примера заданного атрибута таблицы
def get_indexes(table, col, v):
    li = []
    start = 0
    for row in table[col]:
        if row == v:
            index = table[col].index(row, start)
            li.append(index)
            start = index + 1
    return li


# мн-во, полученное после разбиении по атрибуту A
def get_subtable(table, column):
    table_wht_dupl = delete_duplications(table[column])

    return [del_values(table, get_indexes(table, column, v)) for v in table_wht_dupl]


# энтропия множества S
def info(table, column):
    sum = 0

    for value in delete_duplications(table[column]):
        probability = freq(table, column, value) / len(table[column])
        sum += probability * math.log(probability, 2)

    return -sum


# энтропия, полученная после разбиения множества S по атрибуту A
def infox(table, column, result_column):
    sum = 0

    for subtable in get_subtable(table, column):
        sum += (len((subtable[column]))/len(table[column])) * info(subtable, result_column)
    return sum


# для выбора лучшего атрибута считаем критерий прироста информации
def gain(table, column, result_column):
    return info(table, result_column) - infox(table, column, result_column)


# возвращает true, если все элементы уникальные, иначе false
def is_equal(t):
    for i in t:
        if i != t[0]:
            return False
    return True


def c45(table, result):
    col = max([(k, gain(table, k, result)) for k in table.keys() if k != result],
              key=lambda x: x[1])[0]

    tree = []
    for subtable in get_subtable(table, col):
        v = subtable[col][0]
        if is_equal(subtable[result]):
            tree.append(['%s=%s' % (col, v),
                         '%s=%s' % (result, subtable[result][0])])
        else:
            del subtable[col]
            tree.append(['%s=%s' % (col, v)] + c45(subtable, result))
    return tree


create_table()
print(c45(csv_table, 'Play'))