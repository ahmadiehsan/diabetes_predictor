import tensorflow as tf

from framework.utils.configs import c_custom


class ModelCompiler:
    def __init__(self, model):
        self._model = model

    def compile(self):
        self._model.summary()

        optimizer = tf.keras.optimizers.Adam(learning_rate=c_custom['learning_rate'])
        self._model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])

        return self._model
