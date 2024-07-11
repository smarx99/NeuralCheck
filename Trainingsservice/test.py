import unittest
import numpy as np
from keras import models, layers
from unittest.mock import Mock
from App.Service.NetworkService import NetworkService  # Passe den Importweg entsprechend deiner Struktur an

# Dummy-Konfiguration für ein neuronales Netzwerk
class DummyConfiguration:
    def __init__(self, layers, nodes_per_layer, activation_functions):
        self.layers = layers
        self.nodes_per_layer = nodes_per_layer
        self.activation_functions = activation_functions

x_train = np.random.rand(100, 10)  # 100 Datenpunkte mit jeweils 10 Features
y_train = np.random.randint(0, 2, size=(100,))  # Binäre Zielvariablen
x_test = np.random.rand(20, 10)  # 20 Datenpunkte für die Bewertung
y_test = np.random.randint(0, 2, size=(20,))  # Binäre Zielvariablen


class TestNetworkService(unittest.TestCase):
    
    def setUp(self):
        self.service = NetworkService()
        
    def test_create_network(self):
        config = DummyConfiguration(
            layers=3,
            nodes_per_layer=[64, 32, 16],
            activation_functions=['relu', 'relu', 'sigmoid']
        )
        num_features = 10 

        network = self.service.create_network(config, num_features)

        self.assertIsInstance(network, models.Sequential)

        self.assertEqual(len(network.layers), config.layers + 1)
        


if __name__ == '__main__':
    unittest.main()