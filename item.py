import csv

data =[]

def bisItemsExtract(bis_class, bis_specialization):
    data.clear()
    with open('bis.csv') as f:
        for row in csv.reader(f):
            if row[0] == bis_class and row[1] == bis_specialization:
                data.append(row)

    return data