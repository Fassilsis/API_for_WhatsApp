import os


def user_exists(username):
    user_notes_folder = f'notes/{username}'
    return os.path.exists(user_notes_folder)
