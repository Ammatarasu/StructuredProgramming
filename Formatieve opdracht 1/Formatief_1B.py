import pyodbc
from pymongo import MongoClient
import random

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


# Functies die de opdracht uitvoeren


def findrandom():
	"""vind een random item in de SQL databse"""
	fetch = makearray()
	select = fetch[random.randrange(0, len(fetch))]
	return select


def findfar():
	"""Find het product waarvan"""
	originobj = findrandom()
	price = originobj[1]
	currentdiff = 0
	for i in makearray():
		diff = abs(i[1] - price)
		if diff > currentdiff:
			currentdiff = diff
			name = i[0]
			priceobj = i[1]
	return name, priceobj, currentdiff


def averageprice():
	"""berekende de gemmidelde prijs van de producten in de sql server"""
	array = makearray()
	pricelst = []
	val = 0
	c = 0
	for i in array:
		c = c + 1
		val = val + i[1]
		pricelst.append(i[1])
	average = val / c
	return average


# ----------------------------------------------------------------------------------------------------------------------
# Functies die te maken hebben met de SQL server


def sqlinsert(insert):
	"""verwacht een list in de volgorde naam, merk, en prijs. En zet deze in de sql database in tabel product"""
	cursor.execute('SELECT * FROM product')
	cursor.execute('''
                    INSERT INTO product (name, brand, price)
                    VALUES
                    (?, ?, ?)''', insert)
	conn.commit()


def makearray():
	"Zet de data van de sql server om in python lists"
	db = conn.execute('select * from product')
	fetch = db.fetchall()
	array = []
	for i in fetch:
		list = [x for x in i]
		array.append(list)
	return array


# ----------------------------------------------------------------------------------------------------------------------
# Functies die maar 1 keer gebruikt hoeven te worden zolang de MongoDB dataset niet veranderd


def categories():
	"""gaat door de hele MongoDB database en return een list met alle verschillende cagegorieen"""
	categories = []

	for i in finder:
		try:
			category = i['category']
			if category not in categories:
				categories.append(category)
		except KeyError:
			category = "null"
			categories.append(category)
			print('No Category')

	return categories


def findofcat():
	"""door de hele MongoDB Database en zoekt van elke category 1 product en stuurt deze naar de sqlinsert functie om deze in de mssql server te zetten"""
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


# ----------------------------------------------------------------------------------------------------------------------
# Opdracht uivoeren
findofcat()
