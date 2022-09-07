import tensorflow as tf

from framework.utils.configs import c
from framework.utils.path import experiment_path


def load_model():
    model_name = 'best_model.h5'
    experiment = c['use_experiment']
    loaded_model = tf.keras.models.load_model(experiment_path(model_name, experiment))

    return loaded_model
