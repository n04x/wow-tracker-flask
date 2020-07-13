import csv

data =[]

def bisHolyPaladin():
    data.clear()
    with open('holy-pal-bis.csv') as f:
        for row in csv.reader(f):
            data.append(row)

    return data