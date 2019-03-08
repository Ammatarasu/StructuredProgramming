from pymongo import MongoClient
import pyodbc
# connecting to MongoDB server
client = MongoClient()
db = client["databaseopisop"]
products = db['products']
visitors = db['visitors']
sessions = db['sessions']
finder = products.find()
sessfind = sessions.find()
visifind = visitors.find()


# connection to SQL server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-G4E5RU5H;'
                      'Database=opisop;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

def sqlinsert(insert):
	"""verwacht een list in de volgorde naam, merk, en prijs. En zet deze in de sql database in tabel product"""
	cursor.execute('SELECT * FROM product')
	cursor.execute('''
                    INSERT INTO product (name, brand, price)
                    VALUES
                    (?, ?, ?)''', insert)
	conn.commit()


def getcats():
	"""Returns all found categories in the products database"""

	categories = ['Gezond & verzorging', 'Wonen & vrije tijd', 'Huishouden', 'Elektronica & media',
	                 'Kleding & sieraden', 'Eten & drinken', 'Make-up & geuren', 'Baby & kind', None, 'Opruiming',
	                 'Black Friday', 'Cadeau ideeën', 'op=opruiming', '50% korting', 'Nieuw', 'Extra Deals',
	                 ['Make-up & geuren', 'Make-up', 'Nagellak'], 'Folder artikelen']
	return categories

def makearray():
	"Zet de data van de sql server om in python lists"
	db = conn.execute('select * from product')
	fetch = db.fetchall()
	array = []
	for i in fetch:
		list = [x for x in i]
		array.append(list)
	return array


def alreadyinsql(product):
	if product is not None:
		if product in makearray():
			isinsql = True
		else:
			isinsql = False
	else:
		isinsql = True
	return isinsql


def findofcats(numberofprods):
	for i in range(0,numberofprods):
		availablecats = getcats()
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
			if alreadyinsql(name) == False:
				if category in availablecats:
					availablecats.remove(category)
					insert = [name, brand, price]
					sqlinsert(insert)

def getvisitorID():
	for i in visifind:
		visitorid = str(i['_id'])
		conn.execute("""INSERT INTO visitors (visitorID)
						VALUES
						(?)""", visitorid)
		conn.commit()

def getpreviousorder():
	for i in sessfind:

