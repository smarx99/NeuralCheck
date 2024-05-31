class Configuration:
    
    def __init__(self, layers, nodes_per_layer, activation_functions):
        self.layers = layers
        self.nodes_per_layer = nodes_per_layer
        self.activation_functions = activation_functions
        self.result = ''