import pymongo
from pymongo import MongoClient

import pprint


client = MongoClient()
db = client["SP_Formatief_1"]
products = db['products']
profiles = db['profiles']
sessions = db['sessions']

def findFirst():
        pprint.pprint(products.find({}))




def findletter():
        for i in products.find():
                name = i["name"]
                if name[0] == "R":
                        print(name)
                        break

#test


