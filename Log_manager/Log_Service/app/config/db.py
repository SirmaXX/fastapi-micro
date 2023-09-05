from pymongo import MongoClient
import os

DB_URL = os.environ.get('DB_URL')
conn = MongoClient(DB_URL)


# Access your desired database
logdb = conn['webserver_logs']

