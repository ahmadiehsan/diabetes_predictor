import tensorflow as tf

from framework.base.model import IModel
from framework.utils.configs import c_custom


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
        model.summary()

        optimizer = tf.keras.optimizers.Adam(learning_rate=c_custom['learning_rate'])
        model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])

        return model
