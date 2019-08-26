import os


def get_image_path(instance: object, filename: str):
    """
    Get path for /static/photos/{instance_id}/file/{file_name}
    """
    return os.path.join('photos', instance.id, filename)


def get_posters_path(instance: object, filename: str):
    """
    Gets path for event's poster '/static/posters/{event_id}/file/{filename}
    """
    return os.path.join('posters', instance.id, filename)
