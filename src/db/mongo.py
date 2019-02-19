import os

import pymongo

db_url = os.getenv("DB_URL")
db_name = os.getenv("DB_NAME") or "cspheartsync"
client = pymongo.MongoClient(db_url)
db = client[db_name]
