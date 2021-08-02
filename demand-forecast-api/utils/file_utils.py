import os


def create_path_if_not_exists(*args, filename: str) -> str:
    path = os.path.join(*args)
    if not os.path.exists(path):
        os.makedirs(path)

    return os.path.join(path, filename)
