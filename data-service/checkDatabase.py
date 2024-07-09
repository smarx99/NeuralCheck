from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# Konfiguration der MongoDB-Verbindung
app.config["MONGO_URI"] = "mongodb://localhost:27017/data_db"
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
            collection = db[collection_name]
            documents = collection.find({}, {'_id': 1, 'dataset_name': 1, 'username': 1})  # Nur die gewünschten Felder abrufen
            documents_list = list(documents)
            if documents_list:
                empty = False
                print(f"Daten für Sammlung '{collection_name}':")
                for doc in documents_list:
                    print(f"_id: {doc['_id']}, dataset_name: {doc['dataset_name']}, username: {doc['username']}")
                print()
        
        if empty:
            print("Die Datenbank ist leer.")
if __name__ == '__main__':
    with app.app_context():
        # Methode 1: Leeren der Sammlungen
        show_all_entries()