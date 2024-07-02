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
    
    def process_request(self, configurations, dataset_id):
        try:
            print("Processing request with configurations:", configurations)
            self.orchestrator_service.splitting_configs(configurations)
            print("Processed configs:", self.orchestrator_service.training_queue)
            return self.orchestrator_service.training_queue, dataset_id  # Rückgabe der Training Queue und der Dataset ID
            #print("Processing request:", json_request)
            #self.orchestrator_service.splitting_configs(json_request)
            #print("Processed configs:", self.orchestrator_service.training_queue)
            #return self.orchestrator_service.training_queue
        except Exception as e:
            print("An error occurred while processing the request:", e)
            return ''
        
    def receive_results(self, configurations, trainings_url, dataset_id):
        try:
            data_service_url = f"http://127.0.0.1:8004/dataset/{dataset_id}"
            response = requests.get(data_service_url)
            if response.status_code != 200:
                raise Exception("Failed to load dataset from DataService")

            dataset = response.json()["dataset"]

            results = {}
            for i, config in enumerate(configurations):
                print(f"Config before conversion {i+1}:", config_dict)
                config_dict = self.orchestrator_service.configuration_to_dict(config)
                config["dataset"] = dataset["data"]
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
            print("Results before recommendations:", results)
            best_key = self.orchestrator_service.recommend_config(results)
            print("Best configuration key:", best_key)
            return results, best_key
        except Exception as e:
            print("An Error occured during returning results and recommendation: ",e)
            return ''

    # Token Validierung    
    def validate_token(self, token):
        try:
            auth_service_url = "http://localhost:8003/validate-auth"
            response = requests.post(auth_service_url, json={'token': token})
            return response.json()
        except Exception as e:
            print(e)
            return None

        

        