from models.Configuration import Configuration

class OrchestratorService:

    def __init__(self):
        self.training_queue = []

    def splitting_configs(self, configs):
        try:
            print("Splitting configs:", configs)
            self.training_queue = []
            for config in configs:
                layers = len(config['nodes_per_layer'])  # Anzahl der Schichten ist die Länge der nodes_per_layer Liste
                nodes_per_layer = config['nodes_per_layer']  # nodes_per_layer sollte eine Liste sein
                activation_functions = config['activation_functions']
                self.training_queue.append(Configuration(layers, nodes_per_layer, activation_functions))
            print("Training queue:", self.training_queue)
        except Exception as e:
            print("An error occured while splitting the received configs: ", e)
            self.training_queue = Configuration('', '', '')
        print("Splitting configs:", configs) # Logge die aufgeteilten Konfigurationen

    def configuration_to_dict(self, config):
        config_dict = {
            "layers": config.layers,  # layers sollte eine Ganzzahl sein
            "nodes_per_layer": config.nodes_per_layer,  # nodes_per_layer sollte eine Liste sein
            "activation_functions": config.activation_functions,
            "result": config.result
        }
        print("Configuration to dict:", config_dict)
        return config_dict
    
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