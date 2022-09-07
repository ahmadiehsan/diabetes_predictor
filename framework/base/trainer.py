from abc import ABC, abstractmethod

import tensorflow as tf

from framework.utils.configs import c
from framework.utils.path import experiment_path
from framework.utils.save_experiment import ExperimentSaver


class TrainerAbstract(ABC):
    def __init__(self):
        self._fit_result = None

    @property
    def fit_result(self):
        if not self._fit_result:
            raise Exception('First call the fit method')

        return self._fit_result

    def train(self, model, x_train, y_train, x_validation, y_validation):
        self._fit_model(model, x_train, y_train, x_validation, y_validation)

        experiment_saver = ExperimentSaver(model, x_train, y_train, x_validation, y_validation)
        experiment_saver.save()

        self.after_fit_callback()

        experiment_saver.keep_experiment()

    def _fit_model(self, model, x_train, y_train, x_validation, y_validation):
        self._fit_result = model.fit(
            x_train,
            y_train,
            batch_size=c['batch_size'],
            epochs=c['epochs'],
            validation_data=(x_validation, y_validation),
            callbacks=self._get_callbacks_for_fit_model(),
        )

    def _get_callbacks_for_fit_model(self):
        callbacks = [
            tf.keras.callbacks.ModelCheckpoint(experiment_path('best_model.h5'), save_best_only=True),
            tf.keras.callbacks.TensorBoard(log_dir=experiment_path('tensorboard')),
        ]
        callbacks.extend(self.get_fit_callbacks())

        return callbacks

    @abstractmethod
    def get_fit_callbacks(self) -> list:
        pass

    @abstractmethod
    def after_fit_callback(self):
        pass
