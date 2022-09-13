class TrainScript:
    def run(self):
        args = self._get_parsed_args()

        from framework.utils.config_tools import ConfigLoader

        config_loader = ConfigLoader.init_by_args(args)

        from framework.base.data_loaders import ITrainDataLoader
        from framework.base.model import IModel
        from framework.base.trainer import TrainerAbstract

        train_data_loader: ITrainDataLoader = config_loader.get_train_data_loader()
        model: IModel = config_loader.get_model()
        trainer: TrainerAbstract = config_loader.get_trainer()

        x_train, y_train = train_data_loader.get_train_data()
        x_validation, y_validation = train_data_loader.get_validation_data()

        model = model.get_compiled_model()
        trainer.train(model, x_train, y_train, x_validation, y_validation)

    @staticmethod
    def _get_parsed_args():
        import argparse
        from framework.utils.arg_parsers import add_config_file_path_arg, add_custom_configs_arg

        parser = argparse.ArgumentParser()
        add_config_file_path_arg(parser)
        add_custom_configs_arg(parser)
        parser.add_argument('--keep', '-k', help='keep the experiment contents by default', action='store_true')
        parser.add_argument('--epochs', '-e', help='number of epochs', type=int)
        parser.add_argument('--batch-size', '-b', help='batch_size value', type=int)
        parser.add_argument('--model', '-m', help='model path', type=str)
        args = parser.parse_args()

        return args


if __name__ == '__main__':
    TrainScript().run()
