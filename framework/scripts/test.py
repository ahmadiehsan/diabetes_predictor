from framework.utils.arg_parsers import config_file_arg_parser
from framework.utils.config_loader import ConfigLoader
from framework.utils.load_model import load_model


class TestScript:
    @staticmethod
    def run():
        parser = config_file_arg_parser()
        parser.add_argument('--run-for-one', '-o', action='store_true', help='run test for one or all of test set')
        args = parser.parse_args()

        config_loader = ConfigLoader(args.config_file_path)
        configs = config_loader.get_configs()
        data_loader = config_loader.get_data_loader()

        loaded_model = load_model(configs)

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


if __name__ == '__main__':
    TestScript().run()
