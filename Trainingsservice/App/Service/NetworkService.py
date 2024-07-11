from keras import models,layers


class NetworkService:
    def __init__(self):
       pass

    # Create network with given configs
    def create_network(self, configurations, num_features):

        num_layers = configurations.layers
        num_nodes_per_layer = configurations.nodes_per_layer
        activation_function = configurations.activation_functions

        # Create network sequentially
        network = models.Sequential()

        # Adding the input layer
        network.add(layers.Input(shape=(num_features,)))
        
        for i in range(num_layers):
            network.add(layers.Dense(units=num_nodes_per_layer[i], activation=activation_function[i]))

        network.add(layers.Dense(units=1, activation='sigmoid'))
        return network

    # Train network
    def train_network(self, network, x_train, y_train):
        # or adam as optimizer
        network.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        # here batches and epochs can be adapted
        #network.fit(x_train, y_train, batch_size=32, epochs=70)
        network.fit(x_train, y_train, batch_size=32, epochs=20)

        return network

    # Get Accuracy of network
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