import requests
from services.OrchestratorService import OrchestratorService

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
            service = OrchestratorService()
            service.splitting_configs(json_request)
            return service.training_queue
        except Exception as e:
            print("An error occurred while processing the request:", e)
            return ''
        