import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId

class DataService:
    def __init__(self, db):
        self.collection = db.datasets

    # Validate data and return True if so
    def validate_data(self, file):
        try:
            # Set datapointer to the beginning
            file.seek(0)  
            file.seek(0)  

            df = pd.read_csv(file)

            # Check if first column is called "Labels"
            if df.columns[0] != "Labels":
                raise ValueError("The first column must be named 'Labels'.")

            # Check if labels are binary
            unique_labels = df['Labels'].unique()
            if len(unique_labels) != 2:
                raise ValueError("The 'Labels' column must contain exactly two unique values for binary classification.")

            # Check if there are more than 20 rows and mor than 2 columns
            if df.shape[0] < 20 or df.shape[1] < 2:
                raise ValueError("Dataset must have at least 20 samples and 2 features")

            return True
        except Exception as e:
            print(f"Validation error: {str(e)}")
            raise

    # Save data in database
    def save_data(self, username, dataset_name, file):
        # Check if data is validated
        if self.validate_data(file):
            try:
                # Check if data with the same name exists
                existing_dataset = self.collection.find_one({"username": username, "dataset_name": dataset_name})
                if existing_dataset:
                    raise ValueError("This dataset was already uploaded.")

                file.seek(0)  
                df = pd.read_csv(file)
                # Wandle DataFrame in dictionary um  für MongoDB und füge username dazu
                dataset_document = {
                    "dataset_name": dataset_name,
                    "username": username,
                    "data": df.to_dict(orient='records')
                }
                # Save in Mongo DB
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

    # Get datasets names of user
    def get_user_datasets(self, username):
        try:
            datasets = list(self.collection.find({"username": username}, {"data": False}))
            for dataset in datasets:
                dataset["dataset_name"] = str(dataset["dataset_name"])
                dataset["_id"] = str(dataset["_id"])
            return datasets
        except Exception as e:
            raise Exception(f"Failed to retrieve datasets for user '{username}': {str(e)}")

    # Get Content of dataset of user
    def get_dataset_by_dataset_name(self, dataset_name, username):
        try:
            dataset = self.collection.find_one(
            {"dataset_name": dataset_name, "username": username},
            {"data": 1}
            )
            if dataset:
                dataset["_id"] = str(dataset["_id"])
                return dataset
            else:
                raise ValueError(f"Dataset with name '{dataset_name}' not found.")
        except Exception as e:
            raise Exception(f"Failed to retrieve dataset with name '{dataset_name}': {str(e)}")

