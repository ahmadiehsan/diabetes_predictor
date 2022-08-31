import os

from framework.utils.path import ROOT_DIR_ABSOLUTE


def save_model_at(configs, model_name):
    path = os.path.join(ROOT_DIR_ABSOLUTE, 'assets', 'output', configs['model'], model_name)

    return path
