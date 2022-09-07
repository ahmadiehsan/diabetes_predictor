import argparse
import os


def _is_valid_file_argument(arg_parser, arg):
    if not os.path.exists(arg):
        arg_parser.error(f'The file {arg} does not exist!')
    else:
        return arg


def config_file_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_file_path', help='a unix path to the config file', type=lambda x: _is_valid_file_argument(parser, x)
    )

    return parser
