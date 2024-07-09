import pandas as pd
from flask import Flask, request, jsonify
from app.Service.DataHandler import DataHandler
from app.Controller.NetworkController import NetworkController
from app.Service.NetworkService import NetworkService
from app.Model.Configuration import Configuration

app = Flask(__name__)

# Create instances of the classes
data_handler = DataHandler()
network_service = NetworkService()
# configurations = Configuration(3, [30, 14, 1], ['relu', 'relu', 'sigmoid'], 0)
network_controller = NetworkController(network_service)


@app.route('/dataset/<dataset_name>', methods=['GET'])
def get_dataset(dataset_name):
    try:
        df = data_handler.load_dataset(dataset_name)
        return jsonify({"dataset": df.to_dict()}), 200
    except Exception as e:
        print("Error loading dataset:", e)
        return jsonify({"error": "Failed to load dataset"}), 500

@app.route('/prepare_data', methods=['GET'])
def prepare_data():
    data = data_handler.load_dataset()
    prepared_data = data_handler.prepare_data(data)
    return jsonify(prepared_data.head().to_dict()), 200


# just for now
def configuration_to_dict(config):
    return {
        "nodes_per_layer": config.nodes_per_layer,
        "layers": config.layers,
        "activation_functions": config.activation_functions,
        "result": config.result
    }

@app.route('/train', methods=['POST'])
def train_network():
    # Extrahiere die Hyperparameter aus der Anfrage
    data = request.get_json()
    print("Received data for training")  # Log received data

    print("Layers:", data.get('layers'))

    configuration = Configuration(
        layers=data.get('layers'),
        nodes_per_layer=data.get('nodes_per_layer'),
        activation_functions=data.get('activation_functions'),
        result=None
    )
    print("Configuration:", configuration)

    # Load data
    dataset_name = data.get('dataset_name')
    print("Datasetname: ", dataset_name)

    # get username
    username = data.get('username')
    print('Username: ', username)

    df = data_handler.load_dataset(username, dataset_name)

    # Prepare data
    prepared_data = data_handler.prepare_data(df)
    x_train, x_test, y_train, y_test, num_features = data_handler.split_data(prepared_data)

    # Create, train, and evaluate network
    network = network_controller.process(configuration, num_features)
    trained_network = network_service.train_network(network, x_train, y_train)
    test_acc = network_service.evaluate_network(trained_network, x_test, y_test)

    configuration.result = test_acc
    
    # return configuration
    print("Ende Configuration:", configuration)
    return jsonify(configuration_to_dict(configuration)), 200


if __name__ == '__main__':
    app.run(port=8002)