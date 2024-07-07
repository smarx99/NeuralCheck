class Configuration:
    
    def __init__(self, layers, nodes_per_layer, activation_functions):
        self.layers = layers
        self.nodes_per_layer = nodes_per_layer
        self.activation_functions = activation_functions
        self.result = ''

    def to_dict(self):
        config_dict = {
            "layers": self.layers,  # layers sollte eine Ganzzahl sein
            "nodes_per_layer": self.nodes_per_layer,  # nodes_per_layer sollte eine Liste sein
            "activation_functions": self.activation_functions,
            "result": self.result
        }
        return config_dict