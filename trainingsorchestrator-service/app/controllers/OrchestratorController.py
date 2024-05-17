import requests
from models.Configuration import Configuration

class OrchestratorController:

    def __init__(self, url):
        self.url = url

    def receive_request(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  
            return response.json()
        except requests.RequestException as e:
            print("Error fetching request:", e)
            return None 
    
    def process_request(self, json_request):
        try: 
            config = Configuration(json_request.get("nodes_per_layer"), json_request.get("layers"), json_request.get("activation_functions"))
            return config
        except Exception as e:
            print("An error occurred while processing the request:", e)
            return None
        