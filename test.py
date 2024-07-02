from flask import Flask, jsonify
 
app = Flask(__name__)
 
@app.route("/user", methods=['GET'])
def return_configs():
    message = {"first_name": "Jane",
               "last_name": "Doe",
               "username": "JaneDoe",
               "password": "1234"
               }
    return jsonify(message)
 
if __name__ == "__main__":
    app.run(port=8000)