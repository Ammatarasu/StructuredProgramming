import pymongo
from pymongo import MongoClient

import pprint


client = MongoClient()
db = client["SP_Formatief_1"]
products = db['products']
profiles = db['profiles']
sessions = db['sessions']
finder = products.find()

def findFirst():
        """Finds first object in the products collection"""
        object = products.find_one()
        name = object["name"]
        return name



def findletter(letter):
        """"Finds the first instance of a product with the first letter being letter"""
        for i in products.find():
                name = i["name"]
                if name[0] == letter:
                        break
        return name
def averageprice():
        calcprice = []

        for i in finder:
                price = i["price"]["selling_price"]
                calcprice.append(price)
        average = sum(calcprice)/len(calcprice)
        europrice = average / 100
        return europrice


print(findFirst())
print(findletter("R"))
print(averageprice())




