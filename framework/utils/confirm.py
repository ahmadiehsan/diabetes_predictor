def query_yes_no(question, default=None):
    if not default:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError(f'Invalid default answer: {default}')

    valid = {'yes': True, 'y': True, 'ye': True, 'no': False, 'n': False}
    while True:
        choice = input(question + prompt).lower()
        if default and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print('Please respond with [y]es or [n]o')
