import random

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from framework.base.data_loader import IDataLoader
from framework.utils.configs import c
from framework.utils.path import data_path


class DataLoader(IDataLoader):
    csv_x_fields = [
        'pregnant_times',
        'plasma_glucose',
        'blood_pressure',
        'skinfold_thickness',
        'serum_insulin',
        'body_mass_index',
        'pedigree_function',
        'age',
    ]
    csv_y_field = 'class_variable'
    csv_all_fields = [*csv_x_fields, csv_y_field]

    def __init__(self):
        x, y = self._get_x_and_y_dataframes()
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=c['test_size'], random_state=0, shuffle=False
        )

        self.x_train = self._transform(x_train)
        self.y_train = y_train.to_numpy()

        self.x_test = self._transform(x_test)
        self.y_test = y_test.to_numpy()

    def _get_x_and_y_dataframes(self):
        dataframe = pd.read_csv(data_path('pima-indians-diabetes.csv'), names=self.csv_all_fields)
        dataframe.drop_duplicates(inplace=True)

        x = dataframe[self.csv_x_fields]
        y = dataframe[self.csv_y_field]

        return x, y

    @staticmethod
    def _transform(dataframe):
        scaler = StandardScaler()
        result = scaler.fit_transform(dataframe)

        return result

    def get_train_data(self):
        return self.x_train, self.y_train

    def get_validation_data(self):
        return self.get_test_data()

    def get_test_data(self):
        return self.x_test, self.y_test

    def get_one_test_data(self):
        index = random.randint(1, len(self.x_test))

        return self.x_test[index - 1 : index], self.y_test[index - 1 : index]  # return 1 instance but keep it's shape
