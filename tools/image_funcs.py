import os


def get_image_path(images_from):

    def get_profile_image_path(instance: object, filename: str):
        """
        Get path for /static/profile_images/{instance_id}/{file_name}
        """
        return f'{images_from}/{instance}/{filename}'

    return get_profile_image_path
