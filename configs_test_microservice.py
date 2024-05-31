from flask import Flask, jsonify
 
app = Flask(__name__)
 
@app.route("/configs", methods=['GET'])
def return_configs():
    message = [{"layers": 5,
               "nodes_per_layer": [3, 5, 2, 8, 4],
               "activation_functions": ["Sigmoid", "Sigmoid", "ReLU", "Softmax", "Softmax"]},
               {"layers": 2,
                "nodes_per_layer": [2, 5],
               "activation_functions": ["Sigmoid", "Softmax"]},
               {"layers": 4,
                "nodes_per_layer": [5, 2, 8, 4],
               "activation_functions": ["Sigmoid", "ReLU", "Softmax", "Softmax"]}
    ]
    return jsonify(message)
 
if __name__ == "__main__":
    app.run(port=8000)