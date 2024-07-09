from flask import Flask, jsonify
from flask_pymongo import PyMongo
import json

app = Flask(__name__)

# Konfiguration der MongoDB-Verbindung
app.config["MONGO_URI"] = "mongodb://localhost:27017/users_db"
mongo = PyMongo(app)

db = mongo.db
datasets = db.datasets

def show_all_entries():
       # Alle Sammlungen in der Datenbank auflisten
    collections = db.list_collection_names()

    if not collections:
        print("Die Datenbank ist leer.")
    else:
        empty = True
        for collection_name in collections:
            print(f"Collection: {collection_name}")
        collection = db[collection_name]
        # Alle Dokumente in der Sammlung ausgeben
        for document in collection.find():
            print(json.dumps(document, indent=4, default=str))
        print("\n")
        
        if empty:
            print("Die Datenbank ist leer.")
if __name__ == '__main__':
    with app.app_context():
        # Methode 1: Leeren der Sammlungen
        show_all_entries()