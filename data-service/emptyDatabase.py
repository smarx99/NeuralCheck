# Script for emptying the database

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configuration to MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/data_db"
mongo = PyMongo(app)

db = mongo.db
datasets = db.datasets

def clear_db():
    print(datasets.count_documents({}))
    datasets.delete_many({})
    print(datasets.count_documents({}))

if __name__ == '__main__':
    with app.app_context():
        clear_db()