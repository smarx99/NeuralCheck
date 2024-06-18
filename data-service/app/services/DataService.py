# DataService.py
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId

class DataService:
    def __init__(self, db_url, db_name, collection_name):
        # Verbindung mit MongoDB Datenbank
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def validate_data(self, file):

        df = pd.read_csv(file)

        # Überprüfung ob  erste Spalte "Labels" heißt
        if df.columns[0] != "Labels":
            raise ValueError("The first column must be named 'Labels'.")

        # Überprüfung ob Labels binär sind (nur zwei eindeutige Werte enthalten)
        unique_labels = df['Labels'].unique()
        if len(unique_labels) != 2:
            raise ValueError("The 'Labels' column must contain exactly two unique values for binary classification.")

        # Überprüfung ob Datensatz mindestens 20 Zeilen und mindestens 2 weitere Spalten hat
        if df.shape[0] < 20 or df.shape[1] < 2:
            raise ValueError("Dataset must have at least 20 samples and 2 features")

        # True wird zurückgegeben, wenn alle Validierungen erfolgreich waren
        return True

    def save_data(self, username, file):
        # Überprüfe ob datensatz valid ist
        if self.validate_data(file):
            df = pd.read_csv(file)
            # Wandle DataFrame in dictionary um  für MongoDB und füge username dazu
            dataset_document = {
                "username": username,
                "data": df.to_dict(orient='records')
            }
            # Füge datensatz in MongoDB collection ein
            result = self.collection.insert_one(dataset_document)
            return f"Successfully uploaded {len(result.inserted_id)} records"
            # return f"Successfully uploaded dataset with ID: {str(result.inserted_id)}"
        else:
            raise ValueError("Validation failed. Data not saved.")

    def get_user_datasets(self, username):
        try:
            # Rufe datensätze anhand username auf
            datasets = list(self.collection.find({"username": username}, {"data": False}))
            # Konvertiere ObjectId in String für bessere Serialisierung
            for dataset in datasets:
                dataset["_id"] = str(dataset["_id"])
            return datasets
        except Exception as e:
            raise Exception(f"Failed to retrieve datasets for user '{username}': {str(e)}")

    def get_dataset_by_dataset_id(self, dataset_id):
        try:
            # Rufe datensatz anhand dataset_id auf
            dataset = self.collection.find_one({"_id": ObjectId(dataset_id)})
            # Konvertiere ObjectId in String für bessere Serialisierung
            if dataset:
                dataset["_id"] = str(dataset["_id"])
                return dataset
            else:
                raise ValueError(f"Dataset with ID '{dataset_id}' not found.")
        except Exception as e:
            raise Exception(f"Failed to retrieve dataset with ID '{dataset_id}': {str(e)}")

