import joblib

from framework.base.data_loaders import ITestDataLoader
from framework.utils.configs import c
from framework.utils.path import data_path
from framework.utils.path import experiment_path
from src.data_loaders.utils import CSVLoader


class TestDataLoader(ITestDataLoader):
    def __init__(self):
        csv_loader = CSVLoader(data_path('test.csv'))
        x_test = csv_loader.x
        y_test = csv_loader.y

        scaler = self._get_fitted_scaler()

        self.x_test = scaler.transform(x_test)
        self.y_test = y_test.to_numpy()

    @staticmethod
    def _get_fitted_scaler():
        experiment = c['use_experiment']
        scaler = joblib.load(experiment_path('scaler.save', experiment))

        return scaler

    def get_test_data(self):
        return self.x_test, self.y_test

    def get_one_test_data(self, index: int):
        return self.x_test[index - 1 : index], self.y_test[index - 1 : index]  # return 1 instance but keep it's shape
