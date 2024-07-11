import requests
from app.services.DataService import DataService

class DataController:
    def __init__(self, db):
        self.data_service = DataService(db)

    # Uploading data and return message if successfull
    def upload_data(self, username, file):
        try:
            message = self.data_service.save_data(username, file.filename, file)
            return {"message": message}, 200
        except ValueError as e:
            print(f"ValueError: {str(e)}")
            return {"error": str(e)}, 400
        except Exception as e:
            print(f"Exception: {str(e)}")
            return {"error": f"Failed to upload data: {str(e)}"}, 500

    # Get datasets names of user and message if successfull
    def get_user_datasets(self, username):
        try:
            datasets = self.data_service.get_user_datasets(username)
            return {"datasets": datasets}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    # Get content of a dataset and message if successfull
    def get_dataset_by_dataset_name(self, dataset_name, username):
        try:
            dataset = self.data_service.get_dataset_by_dataset_name(dataset_name, username)
            if dataset:
                return {"dataset": dataset}, 200
            else:
                return {"error": "Dataset not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    # Validate Token with Auth Service   
    def validate_token(self, token):
        try:
            auth_service_url = "http://localhost:8003/validate-auth"
            response = requests.post(auth_service_url, json={'token': token})
            return response.json()
        except Exception as e:
            print(e)
            return None
