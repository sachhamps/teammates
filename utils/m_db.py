from pymongo import MongoClient

mongo_client = MongoClient('localhost', 27017)
db = mongo_client['teammates']
players = db['players']
