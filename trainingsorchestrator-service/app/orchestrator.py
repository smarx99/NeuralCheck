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

# just for now
def configurations_to_dict_list(configs):
    return [configuration_to_dict(config) for config in configs]

# just for now
def configurations_to_string_list(configs):
    dic_configs = configurations_to_dict_list(configs)
    return_string = ''
    for config in dic_configs:
        return_string += f"Nodes per layer: {config['nodes_per_layer']}, Layers: {config['layers']}, Activation functions: {config['activation_functions']}"
        return_string += "\n"
    return return_string
 
@app.route("/orch", methods=['GET'])
def print_configs():
    controller = OrchestratorController("http://127.0.0.1:8000/configs")
    request = controller.receive_request()
    configs = controller.process_request(request)
    string_configs = configurations_to_string_list(configs)
    #config_dic = {"Nodes Per Layer": configs.nodes_per_layer, "Number of Layers": configs.layers, "Activation Functions": configs.activation_functions}
    return string_configs

if __name__ == "__main__":
    app.run(port=8001)