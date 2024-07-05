import requests
from services.OrchestratorService import OrchestratorService

class OrchestratorController:

    def __init__(self, url, db):
        self.url = url
        self.orchestrator_service = OrchestratorService(db)
        self.configs = db.configs
    
    def process_request(self, configurations, user, dataset_id):
        try:
            configs = self.orchestrator_service.splitting_configs(configurations)
            self.orchestrator_service.save_configs(configs, user, dataset_id)
            return configs 
        except Exception as e:
            print("An error occurred while processing the request:", e)
            return ''
        
    def receive_results(self, configs, trainings_url, dataset_name):
        try:
            #data_service_url = f"http://127.0.0.1:8004/dataset/{dataset_name}"
            #response = requests.get(data_service_url)
            #if response.status_code != 200:
            #    raise Exception("Failed to load dataset from DataService")

            #dataset = response.json()
            #print("Dataset loaded successfully:", dataset)
            # Debugging-Ausgabe, um zu sehen, was genau in dataset_json ist
            #print("Dataset JSON type:", type(dataset))
            #if isinstance(dataset, list):
            #    print("Dataset JSON list length:", len(dataset))

            results = {}
            #dataset_data = dataset.get("data", [])
            #if not isinstance(dataset_data, list):
            #    raise ValueError("Dataset 'data' field is not a list.")
            for i, config in enumerate(configs):
                print(f"Config before conversion {i+1}:", config)
                config_dict = self.orchestrator_service.configuration_to_dict(config)
                config_dict["dataset_name"] = dataset_name
                print(f"Sending config {i+1} to training service:", config_dict)  # Logge die zu sendenden Konfigurationen
                response = requests.post(trainings_url, json=config_dict)
                if response.status_code == 200:
                    results[f'Config{i+1}'] = response.json()
                else:
                    results[f'Config{i+1}'] = {"error": "Training failed"}
            return results
        except Exception as e:
            print("An Error occured while receiving the results: ", e)
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

        

        