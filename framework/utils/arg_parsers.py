import json
import os


def _is_valid_file_argument(arg_parser, arg):
    if not os.path.exists(arg):
        arg_parser.error(f'The file {arg} does not exist!')
    else:
        return arg


def add_config_file_path_arg(parser):
    parser.add_argument(
        'config_file_path', type=lambda x: _is_valid_file_argument(parser, x), help='a unix path to the config file'
    )


def add_use_experiment_arg(parser):
    parser.add_argument('--use-experiment', '-e', type=str, help='use_experiment value')


def _custom_config_parser(item):
    key, value = item.split('=')

    try:
        value = json.loads(value)
    except json.decoder.JSONDecodeError:
        pass

    return key, value


def add_custom_configs_arg(parser):
    parser.add_argument(
        '--custom-configs',
        '-c',
        metavar='KEY=VALUE',
        nargs='+',
        type=_custom_config_parser,
        help='custom configs in json format',
    )
