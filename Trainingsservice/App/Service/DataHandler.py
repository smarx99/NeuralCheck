from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd


class DataHandler:
    def load_dataset(self):

        # Load the dataset and create a dataframe
        df = pd.read_csv("breast_cancer.csv", index_col="id")

        # print(df.head())
        return df
        # pass

    def prepare_data(self, data):

        df_prepared = data

        # drop duplicates
        df_prepared.drop_duplicates(inplace=True)

        # delete rows with nan values
        # df_prepared = df_prepared.dropna(axis=0)

        # fill columns with nan values
        # column.fillna(column.mean(), inplace=True)

        return df_prepared
        # pass

    def split_data(self, data):

        # define feature and target vector
        x = data.iloc[:, 1:31]
        y = data["diagnosis"]

        # encode categorical target vector
        encoder = LabelEncoder()
        y = encoder.fit_transform(y)

        # conduct train test split
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

        # normalize the data
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)

        return x_train, x_test, y_train, y_test


    