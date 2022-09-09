from abc import ABC, abstractmethod


class ITrainDataLoader(ABC):
    @abstractmethod
    def get_train_data(self):
        pass

    @abstractmethod
    def get_validation_data(self):
        pass


class ITestDataLoader(ABC):
    @abstractmethod
    def get_test_data(self):
        pass

    @abstractmethod
    def get_one_test_data(self, index: int):
        pass
