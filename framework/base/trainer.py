import json
from abc import ABC, abstractmethod

import tensorflow as tf
from numpy import float32

from framework.utils.configs import c
from framework.utils.path import experiment_path


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

        if c['save_experiment']:
            self._save_summary(model, x_train, y_train, x_validation, y_validation)

        self.after_fit_callback()

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
        if c['save_experiment']:
            callbacks = [
                tf.keras.callbacks.ModelCheckpoint(experiment_path('best_model.h5'), save_best_only=True),
                tf.keras.callbacks.TensorBoard(log_dir=experiment_path('tensorboard')),
            ]
        else:
            callbacks = []

        callbacks.extend(self.get_fit_callbacks())

        return callbacks

    @classmethod
    def _save_summary(cls, model, x_train, y_train, x_validation, y_validation):
        with open(experiment_path('summary.txt'), 'w') as file:
            # experiment summary
            file.write('=========================\n')
            file.write('Experiment Summary\n')
            file.write('=====\n')
            file.write(f"Date:\t\t\t\t{c['now']}\n")
            file.write(f"Model path:\t\t\t{c['model']}\n")
            file.write(f"Data loader path:\t{c['data_loader']}\n")
            file.write(f"Trainer path:\t\t{c['trainer']}\n")
            file.write(f'Loss:\t\t\t\t{model.loss}\n')
            file.write(f"Batch size:\t\t\t{c['batch_size']}\n")
            file.write(f"Epochs:\t\t\t\t{c['epochs']}\n")
            file.write(f'Train set:\t\t\t{len(x_train)}\n')
            file.write(f'Validation set:\t\t{len(x_validation)}')

            # model configs
            file.write('\n\n\n\n=========================\n')
            file.write('Model Configs\n')
            file.write('=====\n')
            model.summary(print_fn=lambda x: file.write(x + '\n'))
            file.write('\n' + json.dumps(model.get_config(), indent=2))

            # optimizer configs
            file.write('\n\n\n\n=========================\n')
            file.write('Optimizer Configs\n')
            file.write('=====\n')
            file.write(json.dumps(cls._float32_to_str(model.optimizer.get_config()), indent=2))

            # new line at the end of file
            file.write('\n')

    @classmethod
    def _float32_to_str(cls, data_dictionary: dict):
        new_dict = {}

        for key, value in data_dictionary.items():
            if isinstance(value, dict):
                new_dict[key] = cls._float32_to_str(value)
            else:
                if isinstance(value, float32):
                    new_dict[key] = str(value)
                else:
                    new_dict[key] = value

        return new_dict

    @abstractmethod
    def get_fit_callbacks(self) -> list:
        pass

    @abstractmethod
    def after_fit_callback(self):
        pass
