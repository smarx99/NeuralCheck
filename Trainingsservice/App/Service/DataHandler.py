from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import requests


class DataHandler:
    def load_dataset(self, username, dataset_name):
        try:
            data_service_url = f"http://127.0.0.1:8004/dataset/{username}/{dataset_name}"
            response = requests.get(data_service_url)
            if response.status_code != 200:
                raise Exception(f"Failed to load dataset {dataset_name} from DataService")

            json_response = response.json()
            #print("JSON response from DataService:", json_response)

            # Extract the data from the nested JSON response
            data_list = json_response[0]['dataset']['data']

            # Convert the data to a DataFrame
            df = pd.DataFrame(data_list)

            return df
        except Exception as e:
            print(f"Error loading dataset {dataset_name}:", e)
            return pd.DataFrame()

    def prepare_data(self, data):

        df_prepared = data
        df_prepared.drop_duplicates(inplace=True)

        return df_prepared

    def split_data(self, data):

        # define feature and target vector
        x = data.drop(columns=['Labels'])  # Alle Spalten außer 'Labels'
        y = data['Labels']  # 'Labels' Spalte als Zielvariable

        # count the number of features
        num_features = x.shape[1]

        # encode categorical target vector
        encoder = LabelEncoder()
        y = encoder.fit_transform(y)

        # conduct train test split
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

        # normalize the data
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)

        return x_train, x_test, y_train, y_test, num_features


    