from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from controllers.DataController import DataController

app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen

# Konfiguration der MongoDB-Verbindung
app.config["MONGO_URI"] = "mongodb://localhost:27017/data_db"
mongo = PyMongo(app)

# Datenbank und Sammlung
db = mongo.db
collection = db.datasets
data_controller = DataController(db)


@app.route('/upload_dataset', methods=['POST'])
def upload_data():
    token = validate_token()
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
    token = validate_token()
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

def validate_token():
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
