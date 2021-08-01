import logging
from typing import Any
from utils.file_utils import create_path_if_not_exists
from typehint import FileMode


def create_loggin(path: str = 'logs', name='train', mode: FileMode = 'w', level: Any = logging.INFO):
    console = logging.getLogger(name)

    if mode == 'w':
        for h in console.handlers:
            h.close()
            del h

        console.handlers = []

    if len(console.handlers) == 0:
        fmt = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

        file_path = create_path_if_not_exists(path, filename=f'{name}.log')
        fh = logging.FileHandler(filename=file_path, mode=mode)
        fh.setFormatter(fmt)
        console.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setLevel(level)
        sh.setFormatter(fmt)
        console.addHandler(sh)

    console.setLevel(level)


def get_loggin(path: str = 'logs', name='train', mode: FileMode = 'a', level: Any = logging.INFO):
    console = logging.getLogger(name)

    if len(console.handlers) == 0:
        return create_loggin(path=path, name=name, mode=mode, level=level)

    return console
