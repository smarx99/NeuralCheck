class NetworkController:
    def __init__(self, network_service):
        self.network_service = network_service

    # Receive configuration from training orchestration class
    def receive(self, config):
        self.config = config

    # Send configuration to NetworkService
    def process(self, configuration, num_features):
        return self.network_service.create_network(configuration, num_features)

    # Return the network configuration and result back to the training orchestration class
    def return_result(self, config):
        return self.network_service.configuration_to_dict(config)