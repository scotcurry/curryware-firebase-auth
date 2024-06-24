import os


def get_settings():

    if 'FIREBASE_ADMIN_SDK_JSON' in os.environ:
        firebase_admin_sdk_info = os.environ.get('FIREBASE_ADMIN_SDK_JSON')
    else:
        raise ValueError('FIREBASE_ADMIN_SDK_JSON environment variable not set')

    if 'FIREBASE_DATABASE_NAME' in os.environ:
        firebase_database_name = os.environ.get('FIREBASE_DATABASE_NAME')
    else:
        raise ValueError('FIREBASE_DATABASE_NAME environment variable not set')

    return firebase_admin_sdk_info, firebase_database_name
