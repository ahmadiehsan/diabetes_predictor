import subprocess


class TensorboardScript:
    def run(self):
        args = self._get_parsed_args()

        from framework.utils.config_tools import ConfigLoader

        config_loader = ConfigLoader.init_by_args(args)
        base_configs = config_loader.base_configs

        from framework.utils.path import experiment_path

        experiment = base_configs['use_experiment']
        subprocess.call(f"tensorboard --logdir {experiment_path('tensorboard', experiment)}", shell=True)

    @staticmethod
    def _get_parsed_args():
        import argparse
        from framework.utils.arg_parsers import add_config_file_path_arg, add_use_experiment_arg, add_custom_configs_arg

        parser = argparse.ArgumentParser()
        add_config_file_path_arg(parser)
        add_use_experiment_arg(parser)
        add_custom_configs_arg(parser)
        args = parser.parse_args()

        return args


if __name__ == '__main__':
    TensorboardScript().run()
