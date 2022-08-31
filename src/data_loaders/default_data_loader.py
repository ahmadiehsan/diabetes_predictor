import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from framework.base.data_loader import IDataLoader
from framework.utils.path import ROOT_DIR_ABSOLUTE


class DataLoader(IDataLoader):
    def __init__(self, configs):
        self.configs = configs

        x, y = self._load_x_and_y_from_csv()
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0, shuffle=False)

        scaler = StandardScaler()
        scaler.fit(x)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)

        self.x_train = x_train
        self.y_train = y_train

        self.x_test = x_test
        self.y_test = y_test

    @staticmethod
    def _load_x_and_y_from_csv():
        dataframe = pd.read_csv(
            os.path.join(ROOT_DIR_ABSOLUTE, 'assets', 'data', 'pima-indians-diabetes.csv'),
            names=[
                'pregnant_times',
                'plasma_glucose',
                'blood_pressure',
                'skinfold_thickness',
                'serum_insulin',
                'body_mass_index',
                'pedigree_function',
                'age',
                'class_variable',
            ],
        )
        dataframe.drop_duplicates(inplace=True)

        x = dataframe.iloc[:, :-1].values
        y = dataframe.iloc[:, -1].values

        return x, y

    def get_train_data(self):
        return self.x_train, self.y_train

    def get_dev_data(self):
        return self.get_test_data()

    def get_test_data(self):
        return self.x_test, self.y_test

    def get_one_test_data(self):
        return self.x_test[:1], self.y_test[:1]  # return 1 instance but keep it's shape
