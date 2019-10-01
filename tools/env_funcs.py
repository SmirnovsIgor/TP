import os


def get_env(key, default, type_to_parse=str):
    return type_to_parse(os.environ.get(key, default))
