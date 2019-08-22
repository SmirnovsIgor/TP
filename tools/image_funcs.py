import os


def get_posters_path(instance: object, filename: str):
    """
    Gets path for event's poster '/static/posters/{event_id}/{filename}
    """
    return os.path.join('posters', instance.id, filename)
