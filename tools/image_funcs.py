import os


def get_image_path(instance: object, filename: str):
    return os.path.join('photos', instance.id, filename)