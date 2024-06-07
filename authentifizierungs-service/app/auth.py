from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
 
app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen

# Konfiguration der MongoDB-Verbindung
app.config["MONGO_URI"] = "mongodb://localhost:27017/users_db"
mongo = PyMongo(app)

# Datenbank und Sammlung
db = mongo.db
users = db.users

@app.route("/user", methods=['GET'])
def return_configs():
    message = {
        "first_name": "Jane",
        "last_name": "Doe",
        "username": "JaneDoe",
        "password": "1234"
    }
    return jsonify(message)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({'error': 'The request payload is incomplete.'}), 400

    username = data['username']
    if users.find_one({'username': username}):
        return jsonify({'error': 'Username already exists.'}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = {
        'firstname': data['firstname'],
        'lastname': data['lastname'],
        'username': username,
        'password': hashed_password
    }
    users.insert_one(user)
    return jsonify({'message': 'User registered successfully.'}), 201

if __name__ == '__main__':
    app.run(port=8003)