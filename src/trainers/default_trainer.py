import matplotlib.pyplot as plt

from framework.base.trainer import ITrainer


class Trainer(ITrainer):
    def __init__(self, configs):
        self.configs = configs

    def get_callbacks(self):
        return []

    def display_history(self, history):
        # Accuracy diagram
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Dev'])

        # Loss diagram
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Dev'])

        # space between the plots
        plt.tight_layout()

        plt.show()
