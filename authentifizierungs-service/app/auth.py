from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import jwt
from datetime import datetime, timedelta, timezone
from controllers.AuthController import AuthController
 
app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen
app.config['SECRET_KEY'] = 'imke_lara_steffi'

# Konfiguration der MongoDB-Verbindung
app.config["MONGO_URI"] = "mongodb://localhost:27017/users_db"
mongo = PyMongo(app)

# Datenbank und Sammlung
db = mongo.db
users = db.users
auth_controller = AuthController(db)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    response, status = auth_controller.register_user(data)
    return jsonify(response), status

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = auth_controller.login_user(data)
    if user:
        token = jwt.encode({
            'username': user.username,
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


if __name__ == '__main__':
    app.run(port=8003)