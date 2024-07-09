# DataService.py
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId

class DataService:
    def __init__(self, db):
        # Verbindung mit MongoDB Datenbank
        self.collection = db.datasets
        print("DataService: Initialized with collection:", self.collection.name)

    def validate_data(self, file):
        print("DataService: Initialized with collection:", self.collection.name)
        try:
            file.seek(0)  # Setze den Dateizeiger auf den Anfang

            file.seek(0)  # Setze den Dateizeiger erneut auf den Anfang für pandas

            df = pd.read_csv(file)
            print(f"DataService: DataFrame columns: {df.columns.tolist()}")

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
        except Exception as e:
            print(f"Validation error: {str(e)}")
            raise

    def save_data(self, username, dataset_name, file):
        # Überprüfe ob datensatz valid ist
        if self.validate_data(file):
            try:
                # Überprüfe, ob ein Datensatz mit demselben Namen bereits existiert
                existing_dataset = self.collection.find_one({"username": username, "dataset_name": dataset_name})
                if existing_dataset:
                    raise ValueError("This dataset was already uploaded.")

                file.seek(0)  # Setze den Dateizeiger erneut auf den Anfang für pandas
                df = pd.read_csv(file)
                # Wandle DataFrame in dictionary um  für MongoDB und füge username dazu
                dataset_document = {
                    "dataset_name": dataset_name,
                    "username": username,
                    "data": df.to_dict(orient='records')
                }
                print("DataService: Attempting to insert dataset into MongoDB")
                # Füge datensatz in MongoDB collection ein
                result = self.collection.insert_one(dataset_document)
                if result.acknowledged:
                   print(f"DataService: Successfully uploaded dataset with dataset_name: {dataset_name}")
                else:
                   print("DataService: Insertion not acknowledged")
                return f"Successfully uploaded dataset with dataset_name: {dataset_name}"
            except Exception as e:
                print(f"DataService: Unexpected error: {str(e)}")
                raise
        else:
            raise ValueError("Validation failed. Data not saved.")

    def get_user_datasets(self, username):
        try:
            # Rufe datensätze anhand username auf
            datasets = list(self.collection.find({"username": username}, {"data": False}))
            # Konvertiere ObjectId in String für bessere Serialisierung
            for dataset in datasets:
                dataset["dataset_name"] = str(dataset["dataset_name"])
                dataset["_id"] = str(dataset["_id"])
            return datasets
        except Exception as e:
            raise Exception(f"Failed to retrieve datasets for user '{username}': {str(e)}")

    def get_dataset_by_dataset_name(self, dataset_name, username):
        try:
            # Rufe datensatz anhand dataset_id auf
            dataset = self.collection.find_one(
            {"dataset_name": dataset_name, "username": username},
            {"data": 1}
            )
            # Konvertiere ObjectId in String für bessere Serialisierung
            if dataset:
                dataset["_id"] = str(dataset["_id"])
                return dataset
            else:
                raise ValueError(f"Dataset with name '{dataset_name}' not found.")
        except Exception as e:
            raise Exception(f"Failed to retrieve dataset with name '{dataset_name}': {str(e)}")

