from abc import ABC, abstractmethod


class IDataLoader(ABC):
    @abstractmethod
    def get_train_data(self):
        pass

    @abstractmethod
    def get_validation_data(self):
        pass

    @abstractmethod
    def get_test_data(self):
        pass

    @abstractmethod
    def get_one_test_data(self):
        pass
