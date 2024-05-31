class NetworkController:
    def __init__(self, network_service):
        self.network_service = network_service

    def receive(self, config):
        # Receive configuration from training orchestration class
        self.config = config

    def process(self, configuration):

        # Send configuration to NetworkService
        return self.network_service.create_network(configuration)

    def return_result(self, config):
        # Return the network configuration and result back to the training orchestration class
        return self.network_service.configuration_to_dict(config)
