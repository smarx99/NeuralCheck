import unittest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import pandas as pd
from bson import ObjectId
from app.services.DataService import DataService  # Passe den Importweg entsprechend deiner Struktur an

class TestDataService(unittest.TestCase):

    def setUp(self):
        self.mock_db = Mock()
        self.data_service = DataService(self.mock_db)
        self.mock_file = StringIO("""Labels,Feature1,Feature2
            0,1.0,2.0
            1,2.0,3.0
            0,3.0,4.0
            1,4.0,5.0
            0,5.0,6.0
            1,6.0,7.0
            0,7.0,8.0
            1,8.0,9.0
            0,9.0,10.0
            1,10.0,11.0
            0,11.0,12.0
            1,12.0,13.0
            0,13.0,14.0
            1,14.0,15.0
            0,15.0,16.0
            1,16.0,17.0
            0,17.0,18.0
            1,18.0,19.0
            0,19.0,20.0
            1,20.0,21.0""")

    def test_validate_data_success(self):
        result = self.data_service.validate_data(self.mock_file)
        self.assertTrue(result)

    def test_save_data_existing_dataset(self):
        self.mock_db.datasets.find_one.return_value = {"dataset_name": "testdataset", "username": "testuser"}
        with self.assertRaises(ValueError) as context:
            self.data_service.save_data('testuser', 'testdataset', self.mock_file)
        self.assertEqual(str(context.exception), "This dataset was already uploaded.")

    @patch('app.services.DataService.pd.read_csv')
    def test_save_data_validation_failure(self, mock_read_csv):
        invalid_file = StringIO("""Labels,Feature1
                0,1.0
                1,2.0""")
        mock_read_csv.side_effect = pd.errors.ParserError("Mocked error")
        with self.assertRaises(pd.errors.ParserError):
            self.data_service.save_data('testuser', 'testdataset', invalid_file)

    def test_get_user_datasets(self):
        mock_datasets = [
            {"_id": ObjectId(), "dataset_name": "dataset1", "username": "testuser"},
            {"_id": ObjectId(), "dataset_name": "dataset2", "username": "testuser"}
        ]
        self.mock_db.datasets.find.return_value = mock_datasets
        datasets = self.data_service.get_user_datasets('testuser')
        self.assertEqual(len(datasets), 2)
        self.assertEqual(datasets[0]["dataset_name"], "dataset1")
        self.assertEqual(datasets[1]["dataset_name"], "dataset2")

    def test_get_dataset_by_dataset_name_success(self):
        mock_dataset = {
            "_id": ObjectId(),
            "dataset_name": "testdataset",
            "username": "testuser",
            "data": [{"Labels": 0, "Feature1": 1.0, "Feature2": 2.0}]
        }
        self.mock_db.datasets.find_one.return_value = mock_dataset
        dataset = self.data_service.get_dataset_by_dataset_name('testdataset', 'testuser')
        self.assertIsNotNone(dataset)
        self.assertEqual(dataset["dataset_name"], "testdataset")

if __name__ == '__main__':
    unittest.main()