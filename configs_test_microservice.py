from flask import Flask, jsonify
 
app = Flask(__name__)
 
@app.route("/configs", methods=['GET'])
def return_configs():
    message = [{"nodes_per_layer": 3,
               "layers": 5,
               "activation_functions": ["Sigmoid", "Sigmoid", "ReLu", "Softmax", "Softmax"]},
               {"nodes_per_layer": 4,
               "layers": 2,
               "activation_functions": ["Sigmoid", "Softmax"]},
               {"nodes_per_layer": 7,
               "layers": 4,
               "activation_functions": ["Sigmoid", "ReLu", "Softmax", "Softmax"]}
    ]
    return jsonify(message)
 
if __name__ == "__main__":
    app.run(port=8000)