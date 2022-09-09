import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from framework.base.data_loaders import ITrainDataLoader
from framework.utils.configs import c_custom
from framework.utils.path import data_path
from framework.utils.path import experiment_path
from src.data_loaders.utils import CSVLoader


class TrainDataLoader(ITrainDataLoader):
    def __init__(self):
        csv_loader = CSVLoader(data_path('train.csv'))

        x_train, x_validation, y_train, y_validation = train_test_split(
            csv_loader.x, csv_loader.y, test_size=c_custom['validation_size'], random_state=None, shuffle=True
        )

        scaler = self._get_fitted_scaler(x_train)

        self.x_train = scaler.transform(x_train)
        self.y_train = y_train.to_numpy()

        self.x_validation = scaler.transform(x_validation)
        self.y_validation = y_validation.to_numpy()

    @staticmethod
    def _get_fitted_scaler(x_train):
        scaler = StandardScaler()
        scaler.fit(x_train)

        joblib.dump(scaler, experiment_path('scaler.save'))

        return scaler

    def get_train_data(self):
        return self.x_train, self.y_train

    def get_validation_data(self):
        return self.x_validation, self.y_validation
