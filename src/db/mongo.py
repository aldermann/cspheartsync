import os

import pymongo

db_url = os.getenv("DB_URL") or os.getenv("MONGO_URI") or "localhost"
db_name = os.getenv("DB_NAME") or "cspheartsync"
client = pymongo.MongoClient(db_url)
db = client.get_database() or client.get_database(db_name)
