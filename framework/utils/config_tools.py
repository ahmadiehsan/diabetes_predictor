import datetime
import os.path
from pydoc import locate

import yaml

from framework.utils.singleton_meta import SingletonMeta


class ConfigLoader(metaclass=SingletonMeta):
    def __init__(
        self, config_file_path: str = None, additional_base_configs: dict = None, additional_custom_configs: dict = None
    ):
        if not config_file_path:
            raise Exception('ConfigLoader should at least once initialize with config_file_path')

        additional_base_configs = additional_base_configs if additional_base_configs else {}
        additional_custom_configs = additional_custom_configs if additional_custom_configs else {}

        configs = self._load_configs_from_file(config_file_path)

        base_configs = configs['base']
        self._nested_update(base_configs, {'now': datetime.datetime.now(), **additional_base_configs}, set_empty=False)

        custom_configs = configs['custom']
        self._nested_update(custom_configs, additional_custom_configs, set_empty=False)

        self._base_configs = base_configs
        self._custom_configs = custom_configs

    @classmethod
    def init_by_args(cls, args):
        args_dict = vars(args)
        config_file_path = args_dict.pop('config_file_path')
        custom_configs = args_dict.pop('custom_configs')

        custom_configs_dict = {}
        if custom_configs:
            for config in custom_configs:
                custom_configs_dict[config[0]] = config[1]

        return cls(config_file_path, args_dict, custom_configs_dict)

    @classmethod
    def _load_configs_from_file(cls, config_file_path):
        configs_dir_path = os.path.dirname(config_file_path)

        with open(config_file_path, 'r') as config_file:
            configs = yaml.safe_load(config_file)

        for include in configs.get('includes', []):
            include_file_path = os.path.join(configs_dir_path, include)

            with open(include_file_path, 'r') as include_file:
                cls._nested_update(configs, yaml.safe_load(include_file))

        return configs

    @classmethod
    def _nested_update(cls, dictionary, another_dictionary, set_empty=True):
        for key, value in another_dictionary.items():
            if isinstance(value, dict):
                dictionary[key] = cls._nested_update(dictionary.get(key, {}), value, set_empty)
            else:
                value_is_not_empty = cls._is_not_empty(value)
                if value_is_not_empty or (not value_is_not_empty and set_empty):
                    dictionary[key] = value

        return dictionary

    @staticmethod
    def _is_not_empty(value):
        is_not_empty = False

        try:
            if len(value) >= 1:
                is_not_empty = True
        except TypeError:
            if value is not None:
                is_not_empty = True

        return is_not_empty

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


class ConfigItemGetter:
    def __init__(self, name, configs_dict):
        self.name = name
        self._configs_dict = configs_dict

    def __getitem__(self, item):
        try:
            return self._configs_dict[item]
        except KeyError:
            raise Exception(
                f"Couldn't find the `{item}` item in the `{self.name}` configs, "
                f'please add it into the configs file or fill it through command flags'
            )

    def __str__(self):
        return str(self._configs_dict)
