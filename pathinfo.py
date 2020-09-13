import os


# current dir
def src_dir():
    return os.path.dirname(os.path.realpath(__file__))


# parent dir
def code_dir():
    return os.path.dirname(src_dir())


def log_dir():
    return os.path.join(code_dir(), 'log')


def conf_dir():
    return os.path.join(code_dir(), 'conf')


def conf_file():
    return os.path.join(code_dir(), 'config.ini')


if __name__ == '__main__':
    print('src_dir: ', src_dir())
    print('code_dir: ', code_dir())
    print('log_dir: ', log_dir())
    print('conf_dir: ', conf_dir())
    print('conf_file: ', conf_file())
