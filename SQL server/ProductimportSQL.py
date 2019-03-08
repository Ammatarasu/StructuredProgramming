from pymongo import MongoClient
import pyodbc
# connecting to MongoDB server

client = MongoClient()
db = client["databaseopisop"]
products = db['products']
profiles = db['profiles']
sessions = db['sessions']
finder = products.find()


# connection to SQL server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-G4E5RU5H;'
                      'Database=opisop;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()




def deletesqldata():
	conn.execute('''DELETE products''')
	conn.commit()

def transfertosql(insert):
	conn.execute('''
	INSERT INTO products (name, brand, price, category, sub_category, sub_sub_category,  recommendable, herhaalaankopen)
					VALUES
					(?, ?, ?, ?, ?, ?, ?, ?)''', insert)
	conn.commit()

def importMongo():
	for i in finder:
		try:
			name = i['name']
			category = i['category']
			brand = i['brand']
			heraalaankopen = i['herhaalaankopen']
			recommendable = i['recommendable']
			sub_category = i['sub_category']
			sub_sub_category = i['sub_sub_category']
			price = i['price']['selling_price']
		except KeyError:
			continue
		productprop = [name, brand, price, category, sub_category, sub_sub_category, int(recommendable), int(heraalaankopen)]
		transfertosql(productprop)

importMongo()