# Data.py
from pymongo import MongoClient

class Data:
    def __init__(self, username, data):
        self.username = username
        self.data = data

    def to_dict(self):
        return{
        "username": self.username,
        "data": self.data
        }


