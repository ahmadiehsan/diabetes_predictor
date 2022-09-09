class TrainScript:
    def run(self):
        args = self._get_parsed_args()
        config_loader = self._get_config_loader(args.config_file_path)

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
        from framework.utils.arg_parsers import config_file_arg_parser

        parser = config_file_arg_parser()
        args = parser.parse_args()

        return args

    @staticmethod
    def _get_config_loader(config_file_path):
        from framework.utils.config_loader import ConfigLoader

        config_loader = ConfigLoader(config_file_path)

        return config_loader


if __name__ == '__main__':
    TrainScript().run()
