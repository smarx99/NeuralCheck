import unittest
from app.services.OrchestratorService import OrchestratorService
from app.models.Configuration import Configuration
from unittest.mock import MagicMock

class TestOrchestratorService(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()  # Mock your database connection
        self.service = OrchestratorService(self.db)

    def test_splitting_configs_valid(self):
        configurations = [
            {'layers':3, 'nodes_per_layer': [10, 20, 30], 'activation_functions': ['relu', 'sigmoid', 'softmax']},
            {'layers':2, 'nodes_per_layer': [5, 15], 'activation_functions': ['tanh', 'softmax']}
        ]
        
        result = self.service.splitting_configs(configurations)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].layers, 3)
        self.assertEqual(result[0].nodes_per_layer, [10, 20, 30])
        self.assertEqual(result[0].activation_functions, ['relu', 'sigmoid', 'softmax'])
        self.assertEqual(result[1].layers, 2)
        self.assertEqual(result[1].nodes_per_layer, [5, 15])
        self.assertEqual(result[1].activation_functions, ['tanh', 'softmax'])

    def test_recommend_config(self):
        input_configs = {
            'Config1': {'result': 0.8},
            'Config2': {'result': 0.9},
            'Config3': {'result': 0.85}
        }
        expected_output = 'Config2'
        result = self.service.recommend_config(input_configs)
        self.assertEqual(result, expected_output)

    def test_save_configs(self):
        configs = [
            Configuration(3, [10, 20, 10], ['relu', 'relu', 'sigmoid']),
            Configuration(3, [15, 25, 15], ['tanh', 'tanh', 'softmax'])
        ]
        user = 'test_user'
        dataset_name = 'test_dataset'

        self.service.save_configs(configs, user, dataset_name)
        self.db.configs.insert_one.assert_called_once()

        inserted_data = self.db.configs.insert_one.call_args[0][0]
        self.assertEqual(inserted_data['username'], user)
        self.assertEqual(inserted_data['dataset_name'], dataset_name)
        self.assertEqual(len(inserted_data['configurations']), len(configs))
        for inserted_config, original_config in zip(inserted_data['configurations'], configs):
            self.assertEqual(inserted_config['layers'], original_config.layers)
            self.assertEqual(inserted_config['nodes_per_layer'], original_config.nodes_per_layer)
            self.assertEqual(inserted_config['activation_functions'], original_config.activation_functions)

    if __name__ == '__main__':
        unittest.main()