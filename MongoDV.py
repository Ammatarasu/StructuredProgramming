from pymongo import MongoClient
import datetime
import pprint
client = MongoClient()
db = client.test_database

post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

posts = db.posts
post_id = posts.insert_one(post).inserted_id


pprint.pprint(posts.find_one())
print('github test')

#testing if github actually works now