import json
import os.path
import shutil

import visualkeras
from numpy import float32

from framework.utils.configs import c
from framework.utils.confirm import query_yes_no
from framework.utils.path import experiment_path, first_empty_path, all_experiments_dir_path


class ExperimentSaver:
    def __init__(self, model, x_train, y_train, x_validation, y_validation):
        self.model = model
        self.x_train = x_train
        self.y_train = y_train
        self.x_validation = x_validation
        self.y_validation = y_validation

    def save(self):
        self._save_summary()
        self._save_visualized_model()

    def keep_experiment(self):
        self._rename_current_experiment()
        self._clean_incomplete_experiments()

    def _rename_current_experiment(self):
        if query_yes_no('Do you want to keep the experiment contents?', default='no'):
            experiment_dir_new_path = self._get_experiment_dir_new_path()
            shutil.move(experiment_path(), experiment_dir_new_path)

            print(f'Experiment contents saved at {experiment_dir_new_path}')

    def _get_experiment_dir_new_path(self):
        number_of_model_layers = len(self.model.layers)
        learning_rate = str(self.model.optimizer.get_config()['learning_rate'])
        epochs = c['epochs']

        experiment_dir_new_name = f'L{number_of_model_layers}_R{learning_rate}_E{epochs}'
        experiment_dir_new_path = first_empty_path(all_experiments_dir_path(), experiment_dir_new_name)

        return experiment_dir_new_path

    @staticmethod
    def _clean_incomplete_experiments():
        root_path, directories, files = next(os.walk(all_experiments_dir_path()))
        for directory in directories:
            if directory.startswith('_temp__'):
                shutil.rmtree(os.path.join(root_path, directory), ignore_errors=True)

    def _save_summary(self):
        with open(experiment_path('summary.txt'), 'w') as file:
            # experiment summary
            file.write('=========================\n')
            file.write('Experiment Summary\n')
            file.write('=====\n')
            file.write(f"Date:\t\t\t\t{c['now']}\n")
            file.write(f"Model path:\t\t\t{c['model']}\n")
            file.write(f"Data loader path:\t{c['data_loader']}\n")
            file.write(f"Trainer path:\t\t{c['trainer']}\n")
            file.write(f'Loss:\t\t\t\t{self.model.loss}\n')
            file.write(f"Batch size:\t\t\t{c['batch_size']}\n")
            file.write(f"Epochs:\t\t\t\t{c['epochs']}\n")
            file.write(f'Train set:\t\t\t{len(self.x_train)}\n')
            file.write(f'Validation set:\t\t{len(self.x_validation)}')

            # model configs
            file.write('\n\n\n\n=========================\n')
            file.write('Model Configs\n')
            file.write('=====\n')
            self.model.summary(print_fn=lambda x: file.write(x + '\n'))
            file.write('\n' + json.dumps(self.model.get_config(), indent=2))

            # optimizer configs
            file.write('\n\n\n\n=========================\n')
            file.write('Optimizer Configs\n')
            file.write('=====\n')
            file.write(json.dumps(self._float32_to_str(self.model.optimizer.get_config()), indent=2))

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

    def _save_visualized_model(self):
        visualkeras.graph_view(self.model, to_file=experiment_path('model.png'))
