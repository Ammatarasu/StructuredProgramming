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


def findnumberproducts(number):
    counter = 0
    while counter < number:
        for i in products.find().limit(20):
            name = i['name']
            brand = i['brand']
            price = i['price']['selling_price']

            counter = counter +1
            insertion = [name, brand, price]
            sqlinsert(insertion)

def sqlinsert(insert):
    cursor.execute('SELECT * FROM productprops')
    cursor.execute('''
                    INSERT INTO productprops (name, brand, price)
                    VALUES
                    (?, ?, ?)''', insert)
    conn.commit()


findnumberproducts(15)

