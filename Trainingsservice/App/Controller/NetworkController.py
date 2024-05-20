class NetworkController:
    def __init__(self, network_service):
        self.network_service = network_service

    def receive(self, config):
        # Receive configuration from training orchestration class
        pass

    def process(self, configurations):

        # Send configuration to NetworkService
        return self.network_service.create_network(configurations)

    def return_result(self, config):
        # Return the network configuration and result back to the training orchestration class
        pass
