from abc import ABC, abstractmethod


class IModel(ABC):
    @abstractmethod
    def get_compiled_model(self):
        pass
