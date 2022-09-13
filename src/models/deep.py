import tensorflow as tf

from framework.base.model import IModel
from src.models.utils import ModelCompiler


class Model(IModel):
    def get_compiled_model(self):
        model = tf.keras.Sequential(
            [
                tf.keras.Input(shape=(8,)),
                tf.keras.layers.Dense(4),
                tf.keras.layers.Dense(8),
                tf.keras.layers.Dense(8),
                tf.keras.layers.Dense(4),
                tf.keras.layers.Dense(1, activation='sigmoid'),
            ]
        )
        model_compiler = ModelCompiler(model)

        return model_compiler.compile()
