import pyodbc
from pymongo import MongoClient


#connecting to MongoDB server
client = MongoClient()
db = client["databaseopisop"]
products = db['products']
profiles = db['profiles']
sessions = db['sessions']
finder = products.find()

#connection to SQL server
conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=LAPTOP-G4E5RU5H;'
                        'Database=opisop;'
                        'Trusted_Connection=yes;')

cursor = conn.cursor()


def defineproduct(o):
        i = finder[o]
        name = i['name']
        category = i['category']
        try:
            sub_category = i['sub_category']
        except KeyError:
            sub_category = "null"
        try:
            sub_sub_category = i['sub_sub_category']
        except KeyError:
            sub_sub_category = 'null'
        brand = i['brand']
        price = i['price']['selling_price']
        doelgroep = i['properties']['doelgroep']
        productdetail = [name, brand, price]
        return productdetail

def categories():
    categories = []
    for i in finder:
        try:
            category = i['category']
            if category not in categories:

                categories.append(category)
        except KeyError:
            category = "null"
            print('No Category')

    print(categories)

def sqlinsert(insert):
    cursor.execute('SELECT * FROM product')
    cursor.execute('''
                    INSERT INTO product (name, brand, price)
                    VALUES
                    (?, ?, ?)''', insert)
    conn.commit()

def findofcat():
    availablecats = ['Gezond & verzorging', 'Wonen & vrije tijd', 'Huishouden', 'Elektronica & media',
                     'Kleding & sieraden', 'Eten & drinken', 'Make-up & geuren', 'Baby & kind', None, 'Opruiming',
                     'Black Friday', 'Cadeau ideeën', 'op=opruiming', '50% korting', 'Nieuw', 'Extra Deals',
                     ['Make-up & geuren', 'Make-up', 'Nagellak'], 'Folder artikelen']
    for i in finder:
        try:
            category = i['category']
        except KeyError:
            category = None
        try:
            name = i['name']
        except KeyError:
            name = None
        try:
            brand = i['brand']
        except KeyError:
            brand = None
        try:
            price = i['price']['selling_price']
        except KeyError:
            price = None
        if category in availablecats:
            availablecats.remove(category)
            insert = [name, brand, price]
            sqlinsert(insert)
findofcat()


