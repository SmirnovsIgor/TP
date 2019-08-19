import os


def get_env(key, default, type=str):
    return type(os.environ.get(key, default))