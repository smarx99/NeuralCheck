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