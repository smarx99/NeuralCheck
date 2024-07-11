# Script for emptying database

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# Config to MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/users_db"
mongo = PyMongo(app)

db = mongo.db
users = db.users

def clear_db():
    print(users.count_documents({}))
    users.delete_many({})
    print(users.count_documents({}))

if __name__ == '__main__':
    with app.app_context():
        clear_db()