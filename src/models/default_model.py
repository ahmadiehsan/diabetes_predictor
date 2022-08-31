import tensorflow as tf

from framework.base.model import IModel


class Model(IModel):
    def __init__(self, configs):
        self.configs = configs

    def get_compiled_model(self):
        model = tf.keras.Sequential(
            [
                tf.keras.Input(shape=(8,)),
                tf.keras.layers.Dense(4, activation='relu'),
                tf.keras.layers.Dense(4, activation='relu'),
                tf.keras.layers.Dense(1, activation='sigmoid'),
            ]
        )
        model.summary()
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        return model
