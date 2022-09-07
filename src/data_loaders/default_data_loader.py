import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from framework.base.data_loader import IDataLoader
from framework.utils.configs import c
from framework.utils.path import data_path


class DataLoader(IDataLoader):
    def __init__(self):
        x, y = self._load_x_and_y_from_csv()
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=c['test_size'], random_state=0, shuffle=False
        )

        self.x_train = self._standard_scale(x_train)
        self.y_train = y_train

        self.x_test = self._standard_scale(x_test)
        self.y_test = y_test

    @staticmethod
    def _load_x_and_y_from_csv():
        dataframe = pd.read_csv(
            data_path('pima-indians-diabetes.csv'),
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

    @staticmethod
    def _standard_scale(data_set):
        scaler = StandardScaler()
        data_set = scaler.fit_transform(data_set)

        return data_set

    def get_train_data(self):
        return self.x_train, self.y_train

    def get_validation_data(self):
        return self.get_test_data()

    def get_test_data(self):
        return self.x_test, self.y_test

    def get_one_test_data(self):
        return self.x_test[:1], self.y_test[:1]  # return 1 instance but keep it's shape
