import datetime
import os.path
from pydoc import locate

import yaml

from framework.utils.singleton_meta import SingletonMeta


class ConfigLoader(metaclass=SingletonMeta):
    def __init__(self, config_file_path: str = None):
        if not config_file_path:
            raise Exception('ConfigLoader should at least once initialize with config_file_path')

        configs = self._load_configs(config_file_path)

        self._base_configs = configs['base']
        self._custom_configs = configs['custom']

    @classmethod
    def _load_configs(cls, config_file_path):
        configs_dir_path = os.path.dirname(config_file_path)

        with open(config_file_path, 'r') as config_file:
            configs = yaml.safe_load(config_file)

        for include in configs.get('includes', []):
            include_file_path = os.path.join(configs_dir_path, include)

            with open(include_file_path, 'r') as include_file:
                cls._nested_update(configs, yaml.safe_load(include_file))

        configs['base']['now'] = datetime.datetime.now()

        return configs

    @classmethod
    def _nested_update(cls, dictionary, another_dictionary):
        for key, value in another_dictionary.items():
            if isinstance(value, dict):
                dictionary[key] = cls._nested_update(dictionary.get(key, {}), value)
            else:
                dictionary[key] = value
        return dictionary

    @property
    def base_configs(self):
        return self._base_configs

    @property
    def custom_configs(self):
        return self._custom_configs

    def get_train_data_loader(self):
        train_data_loader_path = self._base_configs['data_loaders']['train']
        train_data_loader_class = locate(f'src.data_loaders.{train_data_loader_path}')

        return train_data_loader_class()  # noqa

    def get_test_data_loader(self):
        test_data_loader_path = self._base_configs['data_loaders']['test']
        test_data_loader_class = locate(f'src.data_loaders.{test_data_loader_path}')

        return test_data_loader_class()  # noqa

    def get_model(self):
        model_path = self._base_configs['model']
        model_class = locate(f'src.models.{model_path}')

        return model_class()  # noqa

    def get_trainer(self):
        trainer_path = self._base_configs['trainer']
        trainer_class = locate(f'src.trainers.{trainer_path}')

        return trainer_class()  # noqa
