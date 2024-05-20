class Configuration:
    
    def __init__(self, nodes_per_layer, layers, activation_functions):
        self.nodes_per_layer = nodes_per_layer
        self.layers = layers
        self.activation_functions = activation_functions
        self.result = ''