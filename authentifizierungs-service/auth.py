from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from app.controllers.AuthController import AuthController


load_dotenv()  # Load environment variables from .env file

 
app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen

# Debug-Ausgabe, um sicherzustellen, dass die Umgebungsvariablen geladen werden
print(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
mongo_uri = os.getenv('MONGO_URI_USERS')
if not mongo_uri:
    raise ValueError("The MONGO_URI_USERS environment variable is not set.")

# Konfiguration der MongoDB-Verbindung
app.config["MONGO_URI"] = mongo_uri
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

@app.route('/user', methods=['GET'])
def get_user():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token is missing!'}), 401
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user = auth_controller.get_user(data)
        if not user:
                return jsonify({'error': 'User not found!'}), 404
        user = user.to_dict()
        user_data = {
                'username': user['username'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
        }
        return jsonify(user_data), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token!'}), 401

@app.route('/validate-auth', methods=['POST'])
def validate_auth():
    token = request.json.get('token')
    if not token:
        return jsonify({'error': 'Token is missing'}), 400
    validation_response = auth_controller.validate_token(token, app.config['SECRET_KEY'])
    if 'error' in validation_response:
        return jsonify(validation_response), 401
    return jsonify({'message': 'Token is valid', 'data': validation_response}), 200


if __name__ == '__main__':
    app.run(port=8003)