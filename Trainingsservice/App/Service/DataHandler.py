from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd


class DataHandler:
    def load_dataset(self, dataset_id):
        try:
            data_service_url = f"http://127.0.0.1:8004/dataset/{dataset_id}"
            response = requests.get(data_service_url)
            if response.status_code != 200:
                raise Exception(f"Failed to load dataset {dataset_id} from DataService")

            df = pd.DataFrame(response.json()["dataset"]["data"])
            # df.set_index("id", inplace=True)  # Falls die ID als Index verwendet werden soll

            return df
        except Exception as e:
            print(f"Error loading dataset {dataset_id}:", e)
            return pd.DataFrame()

    def prepare_data(self, data):

        df_prepared = data

        # drop duplicates
        df_prepared.drop_duplicates(inplace=True)

        # delete rows with nan values
        # df_prepared = df_prepared.dropna(axis=0)

        # fill columns with nan values
        # column.fillna(column.mean(), inplace=True)

        return df_prepared

    def split_data(self, data):

        # define feature and target vector
        x = data.iloc[:, 1:]  # Alle Spalten außer der ersten
        y = data.iloc[:, 0]   # Erste Spalte ist Labels

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


    