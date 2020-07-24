# import csv
import json

data = []

class Materials:
    def __init__(self, item_id, name, mats = dict()):
        self.item_id = item_id
        self.name = name
        self.mats = mats

def matList():
    mats = []
    with open('mats.json') as f:
        data = json.load(f)
        for k in data['items']:
            mats.append(Materials(k, data['items'][k]['name'], data['items'][k]['mats']))
    return mats
