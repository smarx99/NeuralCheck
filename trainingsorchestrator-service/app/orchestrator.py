from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers.OrchestratorController import OrchestratorController
 
app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen

# just for now
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
    controller = OrchestratorController("http://localhost:5173/")
    request_data = request.json
    print("Request data:", request_data)
    configs = controller.process_request(request_data)
    print("Configs:", configs)
    # request = controller.receive_request()
    # configs = controller.process_request(request)

    training_service_url = "http://127.0.0.1:8002/train"

    results = controller.receive_results(configs, training_service_url)

    results, best_key = controller.return_results_recommendations(results)

    response_data = {
        "results": results, 
        "recommended_config": best_key
    }

    print("Response Data:", response_data)  # Logge die Response-Daten zur Überprüfung
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(port=8001)