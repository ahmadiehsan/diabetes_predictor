import subprocess


class TensorboardScript:
    def run(self):
        args = self._get_parsed_args()
        config_loader = self._get_config_loader(args.config_file_path)
        configs = config_loader.configs

        from framework.utils.path import experiment_path

        experiment = configs['use_experiment']
        subprocess.call(f"tensorboard --logdir {experiment_path('tensorboard', experiment)}", shell=True)

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
    TensorboardScript().run()
