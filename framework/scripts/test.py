class TestScript:
    def run(self):
        args = self._get_parsed_args()

        from framework.utils.config_tools import ConfigLoader

        config_loader = ConfigLoader.init_by_args(args)

        from framework.base.data_loaders import ITestDataLoader
        from framework.utils.load_model import load_model

        test_data_loader: ITestDataLoader = config_loader.get_test_data_loader()

        loaded_model = load_model()

        print('\n=============== Test Data')
        if args.run_for_one:
            x_test, y_test = test_data_loader.get_one_test_data(args.run_for_one)
            print(f'Input: {x_test}')
            print(f'Correct answer: {y_test}')
        else:
            x_test, y_test = test_data_loader.get_test_data()
            print(f'Input length: {len(x_test)}')

        print('\n=============== Result')
        if args.run_for_one:
            prediction = loaded_model.predict(x_test)
            print(prediction)
        else:
            loaded_model.evaluate(x_test, y_test, verbose=2)

    @staticmethod
    def _get_parsed_args():
        import argparse
        from framework.utils.arg_parsers import add_config_file_path_arg, add_use_experiment_arg, add_custom_configs_arg

        parser = argparse.ArgumentParser()
        add_config_file_path_arg(parser)
        add_use_experiment_arg(parser)
        add_custom_configs_arg(parser)
        parser.add_argument('--run-for-one', '-o', type=int, help='run test for one or all of test set')
        args = parser.parse_args()

        return args


if __name__ == '__main__':
    TestScript().run()
