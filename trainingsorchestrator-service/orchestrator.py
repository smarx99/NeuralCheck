from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from app.controllers.OrchestratorController import OrchestratorController

# Load environment variables from .env file
load_dotenv() 

app = Flask(__name__)
CORS(app)  

mongo_uri = os.getenv('MONOG_URI_CONFIGS')
if not mongo_uri:
    raise ValueError("The MONGO_URI_CONFIGS environment variable is not set.")

# Configuration to MongoDB
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

# Database and Collection
db = mongo.db
users = db.configs

controller = OrchestratorController("http://localhost:5173/", db)
 
# Get configs, start training and return results
@app.route("/orch", methods=['POST'])
def print_configs():
    # Token Validation
    token = get_token()
    user = token['data']['username']
    
    if(token):
        request_data = request.json
        dataset_name = request_data.get("dataset_name")
        # Check if data is complete
        if not dataset_name:
           return jsonify({'message': 'dataset_name is missing!'}), 400

        configurations = request_data.get("configurations", [])  
        # Split configs and save them
        splitted_configs = controller.process_request(configurations, user, dataset_name)  

        training_service_url = "http://127.0.0.1:8002/train"
        # start trainings and receive accuracy results
        results = controller.receive_results(splitted_configs, training_service_url, dataset_name, user)
        # return results and recommendation
        results, best_key = controller.return_results_recommendations(results)

        response_data = {
            "results": results, 
            "recommended_config": best_key
        }

        print("Response Data:", response_data)  # Logge die Response-Daten zur Überprüfung
        return jsonify(response_data)
    else:
        return jsonify({'message': 'Token validation error!'}), 500

# Get previously used configs of a user   
@app.route('/configs/<username>', methods=['GET'])
def get_previous_configs(username):
    token = get_token()
    user = username

    if(token):
        configs = controller.get_previous_configs(user)
        return jsonify(configs), 200
    else: 
        return jsonify({'message': 'Token validation error!'}), 500

# Validate token
def get_token():
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        token = auth_header.split(" ")[1] if auth_header.startswith("Bearer ") else None
    if not token:
        return jsonify({'message': 'Token is missing!'}), 403
    token = controller.validate_token(token)
    return token   

if __name__ == "__main__":
    app.run(port=8001)