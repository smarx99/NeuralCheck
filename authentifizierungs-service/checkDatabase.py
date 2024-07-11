# help script for checking contents of database

from flask import Flask, jsonify
from flask_pymongo import PyMongo
import json

app = Flask(__name__)

# Config to MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/users_db"
mongo = PyMongo(app)

db = mongo.db
users = db.users

def show_all_entries():
    collections = db.list_collection_names()

    if not collections:
        print("Die Datenbank ist leer.")
    else:
        empty = True
        for collection_name in collections:
            print(f"Collection: {collection_name}")
        collection = db[collection_name]
        for document in collection.find():
            print(json.dumps(document, indent=4, default=str))
        print("\n")
        
        if empty:
            print("Die Datenbank ist leer.")
if __name__ == '__main__':
    with app.app_context():
        show_all_entries()