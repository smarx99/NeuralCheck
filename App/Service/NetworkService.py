from tensorflow.keras import models
from tensorflow.keras import layers


class NetworkService:
    def __init__(self):
        self.config = None
        self.network = None
        self.train_data = None
        self.test_data = None

    def create_network(self, configurations):

        num_layers = configurations.layers
        num_nodes_per_layer = configurations.node_per_layer
        activation_function = configurations.activation_functions

        # create network sequentially
        network = models.Sequential()
        for i in range(num_layers):
            # input_shape = (30,)
            network.add(layers.Dense(units=num_nodes_per_layer[i], activation=activation_function[i]))
            # network.add(Dropout(rate=0.1))

        return network

        pass

    def train_network(self, network, x_train, y_train):

        # or adam as optimizer
        network.compile(optimizer='SGD', loss='categorical_crossentropy', metrics=['accuracy'])
        network.fit(x_train, y_train, batch_size=50, epochs=100)

        return network

    def evaluate_network(self, network, x_test, y_test):

        test_loss, test_acc = network.evaluate(x_test, y_test)

        return test_acc
