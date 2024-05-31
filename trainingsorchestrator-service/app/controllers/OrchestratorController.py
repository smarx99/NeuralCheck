import requests
from services.OrchestratorService import OrchestratorService

class OrchestratorController:

    def __init__(self, url):
        self.url = url
        self.orchestrator_service = OrchestratorService()

    def receive_request(self, request_data):
        try:
            # response = requests.get(self.url)
            # response.raise_for_status()  
            # return response.json()
            return request_data
        except requests.RequestException as e:
            print("Error fetching request:", e)
            return None 
    
    def process_request(self, json_request):
        try: 
            print("Processing request:", json_request)
            self.orchestrator_service.splitting_configs(json_request)
            print("Processed configs:", self.orchestrator_service.training_queue)
            return self.orchestrator_service.training_queue
        except Exception as e:
            print("An error occurred while processing the request:", e)
            return ''
        
    def receive_results(self, configs, trainings_url):
        try:
            results = {}
            for i, config in enumerate(configs):
                print(f"Config before conversion {i+1}:", config)
                config_dict = self.orchestrator_service.configuration_to_dict(config)
                print(f"Sending config {i+1} to training service:", config_dict)  # Logge die zu sendenden Konfigurationen
                response = requests.post(trainings_url, json=config_dict)
                if response.status_code == 200:
                    results[f'Config{i+1}'] = response.json()
                else:
                    results[f'Config{i+1}'] = {"error": "Training failed"}
            return results
        except Exception as e:
            print("An Error occured whule receiving the results: ", e)
            return ''
    
    def return_results_recommendations(self, results):
        try:
            best_key = self.orchestrator_service.recommend_config(results)
            return results, best_key
        except Exception as e:
            print("An Error occured during returning results and recommendation: ",e)
            return ''
        

        