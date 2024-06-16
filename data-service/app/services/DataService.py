# DataService.py
import pandas as pd
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId

class DataService:
    def __init__(self, db_url, db_name, collection_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def validate_data(self, file):

        df = pd.read_csv(file)

        # Überprüfen, ob die erste Spalte "Labels" heißt
        if df.columns[0] != "Labels":
            raise ValueError("The first column must be named 'Labels'.")

        # Überprüfen, ob die Labels binär sind (nur zwei eindeutige Werte enthalten)
        unique_labels = df['Labels'].unique()
        if len(unique_labels) != 2:
            raise ValueError("The 'Labels' column must contain exactly two unique values for binary classification.")

        # Überprüfen, ob der Datensatz mindestens 20 Zeilen und mindestens 2 weitere Spalten hat
        if df.shape[0] < 20 or df.shape[1] < 2:
            raise ValueError("Dataset must have at least 20 samples and 2 features")

        return True

    def save_data(self, username, file):
        # Check if data is valid
        if self.validate_data(file):
            # Read the file again after validation
            df = pd.read_csv(file)
            # Convert DataFrame to dictionary records for insertion and add username
            dataset_document = {
                "username": username,
                "data": df.to_dict(orient='records')
            }
            # Insert data into MongoDB collection
            result = self.collection.insert_one(dataset_document)
            return f"Successfully uploaded {len(result.inserted_id)} records"
        else:
            raise ValueError("Validation failed. Data not saved.")

    def get_user_datasets(self, username):
        datasets = list(self.collection.find({"username": username}, {"data": False}))
        for dataset in datasets:
            dataset["_id"] = str(dataset["_id"])  # Konvertiere ObjectId in String für bessere Serialisierung
        return datasets

    def get_dataset_by_dataset_id(self, dataset_id):
        dataset = self.collection.find_one({"_id": ObjectId(dataset_id)})
        if dataset:
            dataset["_id"] = str(dataset["_id"])  # Konvertiere ObjectId in String für bessere Serialisierung
        return dataset

