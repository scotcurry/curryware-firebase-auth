import os
import base64
import logging


def get_settings():
    FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
              '[dd.service=%(dd.service)s dd.env=%(dd.env)s '
              'dd.version=%(dd.version)s '
              'dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
              '- %(message)s')

    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('curryware-firebase-auth')
    logger.level = logging.DEBUG

    if 'FIREBASE_ADMIN_SDK_JSON' in os.environ:
        logger.error('FIREBASE_ADMIN_SDK_JSON environment variable not set')
        firebase_admin_sdk_info_base64 = os.environ.get('FIREBASE_ADMIN_SDK_JSON')
        firebase_admin_sdk_info_byte = base64.b64decode(firebase_admin_sdk_info_base64)
        firebase_admin_sdk_info = firebase_admin_sdk_info_byte.decode('utf-8')
    else:
        raise ValueError('FIREBASE_ADMIN_SDK_JSON environment variable not set')

    if 'FIREBASE_DATABASE_NAME' in os.environ:
        logger.error('FIREBASE_DATABASE_NAME environment variable not set')
        firebase_database_name_base64 = os.environ.get('FIREBASE_DATABASE_NAME')
        firebase_database_name_byte = base64.b64decode(firebase_database_name_base64)
        firebase_database_name = firebase_database_name_byte.decode('utf-8')
    else:
        raise ValueError('FIREBASE_DATABASE_NAME environment variable not set')

    return firebase_admin_sdk_info, firebase_database_name
