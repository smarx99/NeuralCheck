from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# Konfiguration der MongoDB-Verbindung
app.config["MONGO_URI"] = "mongodb://localhost:27017/configs_db"
mongo = PyMongo(app)

# Datenbank und Sammlung
db = mongo.db
users = db.users

def clear_db():
    # Alle Dokumente in der 'users'-Sammlung löschen
    print(users.count_documents({}))
    users.delete_many({})
    print(users.count_documents({}))

if __name__ == '__main__':
    with app.app_context():
        # Methode 1: Leeren der Sammlungen
        clear_db()