from models.Configuration import Configuration

class OrchestratorService:

    def __init__(self):
        self.training_queue = None

    def splitting_configs(self, json_configs):
        try:
            configs = []
            for json_config in json_configs:
                configs.append(Configuration(json_config.get("nodes_per_layer"), json_config.get("layers"), json_config.get("activation_functions")))
            self.training_queue = configs
        except Exception as e:
            print("An error occured while splitting the received configs: ", e)
            self.training_queue = Configuration('', '', '')

    def configuration_to_dict(self, config):
        return {
            "nodes_per_layer": config.nodes_per_layer,
            "layers": config.layers,
            "activation_functions": config.activation_functions,
            "result": config.result
        }
    
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