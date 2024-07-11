from app.models.Configuration import Configuration

class OrchestratorService:

    def __init__(self, db):
        self.configs = db.configs

    # Split configs and add them to training queue
    def splitting_configs(self, configurations):
        try:
            training_queue = []
            for config in configurations:
                layers = len(config['nodes_per_layer'])  
                nodes_per_layer = config['nodes_per_layer']  
                activation_functions = config['activation_functions']
                training_queue.append(Configuration(layers, nodes_per_layer, activation_functions))
            return training_queue
        except Exception as e:
            print("An error occured while splitting the received configs: ", e)
            training_queue = Configuration('', '', '')
            return training_queue
    
    # Determine best result
    def recommend_config(self, configs):
        try:
            best_key = None
            best_result = float('-inf')
            for key, config in configs.items():
                result = config.get('result', 0)  # Standardwert 0, wenn 'result' nicht vorhanden ist
                if result > best_result:
                    best_key = key
                    best_result = result
            return best_key
        except Exception as e:
            print("An Error occured during returning recommendation: ",e)
            return ''

    # Save configs in database 
    def save_configs(self, configs, user, dataset_name):
        try:
            configs_list = []
            for config in configs:
                configs_list.append(config.to_dict())
            configs_dict = {
                'username': user,
                'dataset_name': dataset_name,
                'configurations': configs_list
            }
            self.configs.insert_one(configs_dict)
        except Exception as e:
            print("An Error occured during saving configs: ",e)

    # Get configs of a user
    def get_configs(self, username):
        configs_data = self.configs.find({'username': username})
        configs = []
        for config_data in configs_data:
            configs.append(config_data['configurations'])
        return configs