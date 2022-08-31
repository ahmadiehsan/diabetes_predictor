import os

import tensorflow as tf

from framework.utils.path import ROOT_DIR_ABSOLUTE


def load_model(configs):
    loaded_model = tf.keras.models.load_model(
        os.path.join(
            ROOT_DIR_ABSOLUTE, 'assets', 'output', configs['model'], f"{configs['use_trained_model']}_model.h5"
        )
    )

    return loaded_model
