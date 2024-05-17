from flask import Flask, jsonify
import requests
from controllers.OrchestratorController import OrchestratorController
 
app = Flask(__name__)
 
# def get_configs():
#     response = requests.get("http://127.0.0.1:8000/configs")
#     return response.json()
 
@app.route("/orch", methods=['GET'])
def print_configs():
    controller = OrchestratorController("http://127.0.0.1:8000/configs")
    request = controller.receive_request()
    configs = controller.process_request(request)
    config_dic = {"Nodes Per Layer": configs.nodes_per_layer, "Number of Layers": configs.layers, "Activation Functions": configs.activation_functions}
    return config_dic

if __name__ == "__main__":
    app.run(port=8001)