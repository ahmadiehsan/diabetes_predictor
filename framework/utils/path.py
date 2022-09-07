import os

from framework.utils.configs import c

_root_dir_absolute = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_assets_path = os.path.join(_root_dir_absolute, 'assets')


def data_path(file_path):
    return os.path.join(_assets_path, 'data', file_path)


def experiment_path(file_path, experiment=None):
    if not experiment:
        experiment = c['now'].strftime('%Y_%m_%d__%H_%M_%S')

    return os.path.join(_assets_path, 'experiments', experiment, file_path)
