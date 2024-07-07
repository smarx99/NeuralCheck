from keras import models,layers


class NetworkService:
    def __init__(self):
        self.config = None
        self.network = None
        self.train_data = None
        self.test_data = None

    def create_network(self, configurations, num_features):

        #print("num features", num_features)
        num_layers = configurations.layers
        #print("Configuration Layers:", num_layers)
        num_nodes_per_layer = configurations.nodes_per_layer
        activation_function = configurations.activation_functions

        # create network sequentially
        network = models.Sequential()

        # adding the input layer
        network.add(layers.Input(shape=(num_features,)))
        
        for i in range(num_layers):
            network.add(layers.Dense(units=num_nodes_per_layer[i], activation=activation_function[i]))
            # network.add(Dropout(rate=0.1)) 

        network.add(layers.Dense(units=1, activation='sigmoid'))
        return network

    def train_network(self, network, x_train, y_train):

        # or adam as optimizer
        network.compile(optimizer='SGD', loss='binary_crossentropy', metrics=['accuracy'])
        network.fit(x_train, y_train, batch_size=32, epochs=70)

        return network

    def evaluate_network(self, network, x_test, y_test):

        test_loss, test_acc = network.evaluate(x_test, y_test)

        return test_acc
    
    def configuration_to_dict(self, config):
            return {
                "layers": config.layers,
                "nodes_per_layer": config.nodes_per_layer,
                "activation_functions": config.activation_functions,
                "result": config.result
            }