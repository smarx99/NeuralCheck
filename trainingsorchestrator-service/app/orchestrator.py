from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from controllers.OrchestratorController import OrchestratorController
 
app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen

# Konfiguration der MongoDB-Verbindung
app.config["MONGO_URI"] = "mongodb://localhost:27017/configs_db"
mongo = PyMongo(app)

# Datenbank und Sammlung
db = mongo.db
users = db.configs

def configuration_to_dict(config):
    config_dict = {
            "layers": config.layers,  # layers sollte eine Ganzzahl sein
            "nodes_per_layer": config.nodes_per_layer,  # nodes_per_layer sollte eine Liste sein
            "activation_functions": config.activation_functions,
            "result": config.result
    }
    print("Configuration to dict:", config_dict)
    return config_dict

def configurations_to_dict(configs):
    return {
        f'Config{i+1}': configuration_to_dict(config)
        for i, config in enumerate(configs)
    }
 
@app.route("/orch", methods=['POST'])
def print_configs():
    controller = OrchestratorController("http://localhost:5173/", db)
    # Token Validierung
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        token = auth_header.split(" ")[1] if auth_header.startswith("Bearer ") else None
    if not token:
        return jsonify({'message': 'Token is missing!'}), 403
    token = controller.validate_token(token)
    user = token['data']['username']
    if(token):
        request_data = request.json
        print("Request data:", request_data)

        dataset_name = request_data.get("dataset_name")
        if not dataset_name:
           return jsonify({'message': 'dataset_name is missing!'}), 400

        configurations = request_data.get("configurations", [])  # Konfigurationen aus dem Datenobjekt
        splitted_configs = controller.process_request(configurations, user, dataset_id)  

        training_service_url = "http://127.0.0.1:8002/train"

        results = controller.receive_results(splitted_configs, training_service_url, dataset_id)

        results, best_key = controller.return_results_recommendations(results)

        response_data = {
            "results": results, 
            "recommended_config": best_key
        }

        print("Response Data:", response_data)  # Logge die Response-Daten zur Überprüfung
        return jsonify(response_data)
    else:
        return jsonify({'message': 'Token validation error!'}), 500

if __name__ == "__main__":
    app.run(port=8001)