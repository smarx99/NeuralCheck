from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers.DataController import DataController

app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen

# Konfiguration der MongoDB-Verbindung
DB_URI = "mongodb://localhost:27017"
DB_NAME = "data_db"
COLLECTION_NAME = "datasets"

# Initialisiere DataController
data_controller = DataController(DB_URI, DB_NAME, COLLECTION_NAME)

@app.route('/upload', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    username = request.form.get('username')  # Annahme: Username wird übermittelt

    response, status = data_controller.upload_data(username, file)
    return jsonify(response), status

@app.route('/datasets/<username>', methods=['GET'])
def get_user_datasets(username):
    response, status = data_controller.get_user_datasets(username)
    return jsonify(response), status

@app.route('/dataset/<dataset_id>', methods=['GET'])
def get_dataset_by_dataset_id(dataset_id):
    response, status = data_controller.get_dataset_by_dataset_id(dataset_id)
    return jsonify(response), status

if __name__ == '__main__':
    app.run(port=8004)
