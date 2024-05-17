from flask import Flask, jsonify
 
app = Flask(__name__)
 
@app.route("/configs", methods=['GET'])
def return_configs():
    message = {"nodes_per_layer": 3,
               "layers": 5,
               "activation_functions": ["Sigmoid", "Sigmoid", "ReLu", "Softmax", "Softmax"]}
    return jsonify(message)
 
if __name__ == "__main__":
    app.run(port=8000)