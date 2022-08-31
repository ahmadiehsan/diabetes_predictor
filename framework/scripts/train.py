import tensorflow as tf

from framework.utils.arg_parsers import config_file_arg_parser
from framework.utils.config_loader import ConfigLoader
from framework.utils.save_model import save_model_at


class TrainScript:
    def run(self):
        args = config_file_arg_parser().parse_args()

        config_loader = ConfigLoader(args.config_file_path)
        configs = config_loader.get_configs()
        data_loader = config_loader.get_data_loader()
        model = config_loader.get_model()
        trainer = config_loader.get_trainer()

        x_train, y_train = data_loader.get_train_data()
        x_dev, y_dev = data_loader.get_dev_data()

        model = model.get_compiled_model()
        history = model.fit(
            x_train,
            y_train,
            batch_size=configs['batch_size'],
            epochs=configs['epochs'],
            validation_data=(x_dev, y_dev),
            callbacks=[*trainer.get_callbacks(), *self._get_callbacks(configs)],
        )
        self._save_last_model(model, configs)
        trainer.display_history(history)

    @staticmethod
    def _get_callbacks(configs):
        callbacks = [tf.keras.callbacks.ModelCheckpoint(save_model_at(configs, 'best_model.h5'), save_best_only=True)]

        return callbacks

    @staticmethod
    def _save_last_model(model, configs):
        model.save(save_model_at(configs, 'last_model.h5'))


if __name__ == '__main__':
    TrainScript().run()
