import requests
from services.DataService import DataService

class DataController:
    def __init__(self, db):
        self.data_service = DataService(db)

    def upload_data(self, username, file):
        try:
            print(f"DataController: Uploading dataset for user: {username}, file: {file.filename}")
            # Speichern des Datensatzes und message Rückmeldung von DataService
            message = self.data_service.save_data(username, file.filename, file)
            return {"message": message}, 200
        except ValueError as e:
            print(f"ValueError: {str(e)}")
            # Fehlermeldung falls Fehler während upload
            return {"error": str(e)}, 400
        except Exception as e:
            print(f"Exception: {str(e)}")
            # Fehlermeldung bei anderen Fehlern
            return {"error": f"Failed to upload data: {str(e)}"}, 500


    def get_user_datasets(self, username):
        try:
            # Abrufen der Datensätze des users
            datasets = self.data_service.get_user_datasets(username)
            return {"datasets": datasets}, 200
        except Exception as e:
            # Fehlermeldung wenn Fehler während Abrufens der Datensätze
            return {"error": str(e)}, 400

    def get_dataset_by_dataset_name(self, dataset_name, username):
        try:
            # Abrufen des Datensatzes anhand dataset_name
            dataset = self.data_service.get_dataset_by_dataset_name(dataset_name, username)
            if dataset:
                return {"dataset": dataset}, 200
            else:
                # Fehlermeldung wenn Datensatz nicht gefunden
                return {"error": "Dataset not found"}, 404
        except Exception as e:
            # Fehlermeldung wenn Fehler während Abrufens des Datensatzes
            return {"error": str(e)}, 400
        
    def validate_token(self, token):
        try:
            auth_service_url = "http://localhost:8003/validate-auth"
            response = requests.post(auth_service_url, json={'token': token})
            return response.json()
        except Exception as e:
            print(e)
            return None