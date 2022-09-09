import matplotlib.pyplot as plt

from framework.base.trainer import TrainerAbstract
from framework.utils.path import experiment_path


class Trainer(TrainerAbstract):
    def get_fit_callbacks(self) -> list:
        return []

    def after_fit_callback(self):
        # Accuracy diagram
        plt.subplot(1, 2, 1)
        plt.plot(self.fit_result.history['val_accuracy'])
        plt.plot(self.fit_result.history['accuracy'])
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Validation', 'Train'])

        # Loss diagram
        plt.subplot(1, 2, 2)
        plt.plot(self.fit_result.history['val_loss'])
        plt.plot(self.fit_result.history['loss'])
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Validation', 'Train'])

        # space between the plots
        plt.tight_layout()

        # save
        save_at = experiment_path('accuracy_and_loss.png')
        plt.savefig(save_at)

        # show
        plt.show()
