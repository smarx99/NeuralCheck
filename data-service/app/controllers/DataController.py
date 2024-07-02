from services.DataService import DataService

class DataController:
    def __init__(self, db):
        self.data_service = DataService(db)

    def upload_data(self, username, file):
        try:
            print(f"DataController: Uploading dataset for user: {username}, file: {file.filename}")
            # Speichern des Datensatzes und message Rückmeldung von DataService
            message = self.data_service.save_data(username, file)
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

    def get_dataset_by_dataset_id(self, dataset_id):
        try:
            # Abrufen des Datensatzes anhand dataset_id
            dataset = self.data_service.get_dataset_by_dataset_id(dataset_id)
            if dataset:
                return {"dataset": dataset}, 200
            else:
                # Fehlermeldung wenn Datensatz nicht gefunden
                return {"error": "Dataset not found"}, 404
        except Exception as e:
            # Fehlermeldung wenn Fehler während Abrufens des Datensatzes
            return {"error": str(e)}, 400