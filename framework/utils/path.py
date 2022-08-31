import os


def is_valid_file_argument(arg_parser, arg):
    if not os.path.exists(arg):
        arg_parser.error(f'The file {arg} does not exist!')
    else:
        return arg


def _root_dir_absolute():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


ROOT_DIR_ABSOLUTE = _root_dir_absolute()
