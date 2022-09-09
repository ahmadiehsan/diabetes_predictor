import os

from framework.utils.configs import c

_root_dir_absolute = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_assets_path = os.path.join(_root_dir_absolute, 'assets')


def data_path(file_path):
    return os.path.join(_assets_path, 'data', file_path)


def all_experiments_dir_path():
    return os.path.join(_assets_path, 'experiments')


def experiment_path(file_path=None, experiment=None):
    is_read_mode = bool(experiment)

    if not is_read_mode:
        now_formatted = c['now'].strftime('%Y_%m_%d__%H_%M_%S')
        experiment = f'_temp__{now_formatted}'

    experiment_dir_path = os.path.join(all_experiments_dir_path(), experiment)

    if not os.path.exists(experiment_dir_path):
        if is_read_mode:
            raise Exception(f"The `{experiment}` experiment doesn't exist, check the `use_experiment` value")
        else:
            os.makedirs(experiment_dir_path)

    if file_path:
        return os.path.join(experiment_dir_path, file_path)
    else:
        return experiment_dir_path


def first_empty_path(parent_dir_path, dir_name):
    dir_path = os.path.join(parent_dir_path, dir_name)

    counter = 2
    while os.path.exists(dir_path):
        dir_path = os.path.join(parent_dir_path, f'{dir_name}_{counter}')
        counter += 1

    return dir_path
