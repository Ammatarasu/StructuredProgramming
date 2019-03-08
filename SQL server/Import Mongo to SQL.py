from pymongo import MongoClient
import pyodbc
# connecting to MongoDB server

client = MongoClient()
db = client["databaseopisop"]
products = db['products']
profiles = db['profiles']
sessions = db['sessions']
findsessions = sessions.find()


# connection to SQL server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-G4E5RU5H;'
                      'Database=opisop;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

def importsessions():
	for i in findsessions:
		try:
			visitorID = i['_id']
			browser = i['user_agent']['browser']['familiy']
			device = i['user_agent']['device']['family']
			isMobile = i['user_agent']['flags']['is_mobile']
			isPC = i['user_agent']['flags']['is_pc']
			session_start = i['session_start']
			session_end = i['session_end']
		except KeyError:
			continue
		sessioninsert = [visitorID, browser, device, int(isMobile), int(isPC), session_start, session_end]
		insertintosessions(sessioninsert)


def insertintosessions(insert):
	conn.execute('''INSERT INTO sessions (visitorID, browser, device, isMobile, isPC, session_start, session_end)
					VALUES
					(?,?,?,?,?,?,?)''', insert)
	conn.commit()

def MDfindtags(collection):
	tags = []
	for i in db[collection]:
