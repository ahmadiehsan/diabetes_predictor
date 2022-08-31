import argparse

from framework.utils.path import is_valid_file_argument


def config_file_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_file_path', help='a unix path to the config file', type=lambda x: is_valid_file_argument(parser, x)
    )

    return parser
