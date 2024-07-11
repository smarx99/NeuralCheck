# Script for emptying the database

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configuration to MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/configs_db"
mongo = PyMongo(app)

db = mongo.db
configs = db.configs

def clear_db():
    print(configs.count_documents({}))
    configs.delete_many({})
    print(configs.count_documents({}))

if __name__ == '__main__':
    with app.app_context():
        clear_db()