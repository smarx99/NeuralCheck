from services.DataService import DataService

class DataController:
    def __init__(self, db_url, db_name, collection_name):
        self.data_service = DataService(db_url, db_name, collection_name)

    def upload_data(self, username, file):
        if file:
            try:
                message = self.data_service.save_data(username, file)
                return {"message": message}, 200
            except ValueError as e:
                return {"error": str(e)}, 400
        return {"error": "No file provided"}, 400

    def get_user_datasets(self, username):
        try:
            datasets = self.data_service.get_user_datasets(username)
            return {"datasets": datasets}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    def get_dataset_by_dataset_id(self, dataset_id):
        try:
            dataset = self.data_service.get_dataset_by_dataset_id(dataset_id)
            if dataset:
                return {"dataset": dataset}, 200
            else:
                return {"error": "Dataset not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400