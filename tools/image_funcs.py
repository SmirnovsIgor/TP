import os


def get_image_path(instance: object, filename: str):
    """
    Get path for /static/photos/{instance_id}/file/{file_name}
    """
    return os.path.join('photos', instance.id, filename)
