import requests
from services.OrchestratorService import OrchestratorService

class OrchestratorController:

    def __init__(self, url, db):
        self.url = url
        self.orchestrator_service = OrchestratorService(db)
        self.configs = db.configs
    
    def process_request(self, configurations, user, dataset_name):
        try:
            configs = self.orchestrator_service.splitting_configs(configurations)
            self.orchestrator_service.save_configs(configs, user, dataset_name)
            return configs 
        except Exception as e:
            print("An error occurred while processing the request:", e)
            return ''
        
    def receive_results(self, configs, trainings_url, dataset_name, username):
        try:
            results = {}
            for i, config in enumerate(configs):
                print(f"Config before conversion {i+1}:", config)
                config_dict = config.to_dict()
                print(f"Sending config {i+1} to training service:", config_dict)  # Logge die zu sendenden Konfigurationen
                configs_data_user = config_dict
                configs_data_user['dataset_name'] = dataset_name
                configs_data_user['username'] = username
                response = requests.post(trainings_url, json=configs_data_user)
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

    def validate_token(self, token):
        try:
            auth_service_url = "http://localhost:8003/validate-auth"
            response = requests.post(auth_service_url, json={'token': token})
            return response.json()
        except Exception as e:
            print(e)
            return None
    
    def get_previous_configs(self, username):
        try:
            configs = self.orchestrator_service.get_configs(username)
            return configs
        except Exception as e:
            print("An error occured while getting the configs: ",e)
            return {'error': 'Error while getting the configs'}, 400

        

        