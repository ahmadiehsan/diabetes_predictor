from abc import ABC, abstractmethod


class ITrainer(ABC):
    @abstractmethod
    def get_callbacks(self):
        pass

    @abstractmethod
    def display_history(self, history):
        pass
