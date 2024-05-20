from flask import Flask, request, jsonify
from App.Controller.NetworkController import NetworkController
from App.Service.DataHandler import DataHandler
from App.Service.NetworkService import NetworkService
from App.Model.Configuration import Configuration

app = Flask(__name__)

# Create instances of the classes
data_handler = DataHandler()
network_service = NetworkService()
configurations = Configuration(3, [30, 14, 1], ['relu', 'relu', 'sigmoid'], 0)
network_controller = NetworkController(network_service)


@app.route('/load_data', methods=['GET'])
def load_data():
    data = data_handler.load_dataset()
    return jsonify(data.head().to_dict()), 200


@app.route('/prepare_data', methods=['GET'])
def prepare_data():
    data = data_handler.load_dataset()
    prepared_data = data_handler.prepare_data(data)
    return jsonify(prepared_data.head().to_dict()), 200


@app.route('/train', methods=['GET'])
def train_network():
    request_data = request.get_json()
    configurations = Configuration(
        layers=request_data['layers'],
        node_per_layer=request_data['node_per_layer'],
        activation_functions=request_data['activation_functions'],
        result=0
    )

    # Load and prepare data
    data = data_handler.load_dataset()
    prepared_data = data_handler.prepare_data(data)
    x_train, x_test, y_train, y_test = data_handler.split_data(prepared_data)

    # Create, train, and evaluate network
    network = network_controller.process(configurations)
    trained_network = network_service.train_network(network, x_train, y_train)
    test_acc = network_service.evaluate_network(trained_network, x_test, y_test)

    result = {
        'test_acc': test_acc
    }
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(port=8001)