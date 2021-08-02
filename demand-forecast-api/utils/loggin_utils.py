import logging
from time import time
from typing import Any
from utils.file_utils import create_path_if_not_exists
from typehint import FileMode
import contextlib


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
    
    return console


def get_loggin(path: str = 'logs', name='train', mode: FileMode = 'a', level: Any = logging.INFO):
    console = logging.getLogger(name)

    if len(console.handlers) == 0:
        return create_loggin(path=path, name=name, mode=mode, level=level)

    return console


@contextlib.contextmanager
def timer(console: logging.Logger = None, loggin_name: str = None, message_prefix: str = ''):

    if console is None:
        console = get_loggin(name=loggin_name)

    start_time = time()

    try:
        yield console
        console.info(f'{message_prefix} ET: {calculate_elapsed_time(start_time)}')
    except Exception as ex:
        console.exception(f'EXCEPTION {message_prefix} ET: {calculate_elapsed_time(start_time)}')
        raise ex


def calculate_elapsed_time(start_time: float):
    et = time() - start_time

    minutes = et/60

    if minutes < 1:
        return f'{et:.03f}s'
    else:
        hour = minutes / 60
        if hour < 1:
            return f'{minutes:.03f}m'
        else:
            return f'{hour:.03f}h'
