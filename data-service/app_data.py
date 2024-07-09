import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import io
from werkzeug.datastructures import FileStorage
from app.controllers.DataController import DataController

load_dotenv()
print(os.getenv('MONGO_URI_DATA'))

app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen

# Konfiguration der MongoDB-Verbindung
mongo_uri = os.getenv('MONGO_URI_DATA')
if not mongo_uri:
    raise ValueError("The MONGO_URI_DATA environment variable is not set.")

app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

# Datenbank und Sammlung
db = mongo.db
collection = db.datasets
data_controller = DataController(db)

@app.route('/default_dataset', methods=['GET'])
def load_default_dataset():
    username = request.args.get('username')
    csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data-service/breast_cancer_valid.csv')
    with open(csv_file_path, 'rb') as file:
        csv_content = file.read()
        csv_file = io.BytesIO(csv_content)
        file = FileStorage(stream=csv_file, filename="breast_cancer_valid.csv", content_type="text/csv")
    response, status = data_controller.upload_data(username, file)
    return jsonify(response), status

@app.route('/upload_dataset', methods=['POST'])
def upload_data():
    token = get_token()
    token = data_controller.validate_token(token)
    if(token):
        file = request.files['file']
        username = request.form['username']
        print(f"Received file: {file.filename}, username: {username}")
        try:
            response, status = data_controller.upload_data(username, file)
            return jsonify(response), status
        except KeyError as e:
                print(f"Missing required parameter: {str(e)}")
                return jsonify({'error': f'Missing required parameter: {str(e)}'}), 400
        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'message': 'Token validation error!'}), 500

@app.route('/datasets/<username>', methods=['GET'])
def get_user_datasets(username):
    token = get_token()
    if(token):
        try:
            datasets = data_controller.get_user_datasets(username)
            return jsonify(datasets), 200
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({'message': 'Token validation error!'}), 500

@app.route('/dataset/<username>/<dataset_name>', methods=['GET'])
def get_dataset_by_dataset_name(dataset_name, username):
    try:
        dataset = data_controller.get_dataset_by_dataset_name(dataset_name, username)
        return jsonify(dataset), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_token():
    # Token Validierung
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        token = auth_header.split(" ")[1] if auth_header.startswith("Bearer ") else None
    if not token:
        return jsonify({'message': 'Token is missing!'}), 403
    token = data_controller.validate_token(token)
    return token

if __name__ == '__main__':
    app.run(port=8004)