class TestScript:
    def run(self):
        args = self._get_parsed_args()
        config_loader = self._get_config_loader(args.config_file_path)

        from framework.base.data_loader import IDataLoader
        from framework.utils.load_model import load_model

        data_loader: IDataLoader = config_loader.get_data_loader()

        loaded_model = load_model()

        print('\n=============== Test Data')
        if args.run_for_one:
            x_test, y_test = data_loader.get_one_test_data()
            print(f'Input: {x_test}')
            print(f'Correct answer: {y_test}')
        else:
            x_test, y_test = data_loader.get_test_data()
            print(f'Input length: {len(x_test)}')

        print('\n=============== Result')
        if args.run_for_one:
            prediction = loaded_model.predict(x_test)
            print(prediction)
        else:
            loaded_model.evaluate(x_test, y_test, verbose=2)

    @staticmethod
    def _get_parsed_args():
        from framework.utils.arg_parsers import config_file_arg_parser

        parser = config_file_arg_parser()
        parser.add_argument('--run-for-one', '-o', action='store_true', help='run test for one or all of test set')
        args = parser.parse_args()

        return args

    @staticmethod
    def _get_config_loader(config_file_path):
        from framework.utils.config_loader import ConfigLoader

        config_loader = ConfigLoader(config_file_path)

        return config_loader


if __name__ == '__main__':
    TestScript().run()
