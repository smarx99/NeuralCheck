# Data.py
from pymongo import MongoClient

class Data:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_data(self, data):
        result = self.collection.insert_one(data)
        return result.inserted_id

    def get_data(self):
        data = self.collection.find_one()
        return data


