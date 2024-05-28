from flask import Flask, jsonify
import requests
from controllers.OrchestratorController import OrchestratorController
 
app = Flask(__name__)

# just for now
def configuration_to_dict(config):
    return {
        "nodes_per_layer": config.nodes_per_layer,
        "layers": config.layers,
        "activation_functions": config.activation_functions,
        "result": config.result
    }

def configurations_to_dict(configs):
    return {
        f'Config{i+1}': configuration_to_dict(config)
        for i, config in enumerate(configs)
    }
 
@app.route("/orch", methods=['GET'])
def print_configs():
    controller = OrchestratorController("http://127.0.0.1:8000/configs")
    request = controller.receive_request()
    configs = controller.process_request(request)

    training_service_url = "http://127.0.0.1:8002/train"

    results = controller.receive_results(configs, training_service_url)

    results = controller.return_results_recommendations(results)

    return jsonify(results)

if __name__ == "__main__":
    app.run(port=8001)