from pydoc import locate

import yaml


class ConfigLoader:
    def __init__(self, config_file_path: str):
        self._configs = yaml.safe_load(open(config_file_path, 'r'))

    def get_configs(self):
        return self._configs

    def get_data_loader(self):
        data_loader_path = self._configs['data_loader']
        data_loader_class = locate(f'src.data_loaders.{data_loader_path}')

        return data_loader_class(self._configs)  # noqa

    def get_model(self):
        model_path = self._configs['model']
        model_class = locate(f'src.models.{model_path}')

        return model_class(self._configs)  # noqa

    def get_trainer(self):
        trainer_path = self._configs['trainer']
        trainer_class = locate(f'src.trainers.{trainer_path}')

        return trainer_class(self._configs)  # noqa
