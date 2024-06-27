import os
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
        firebase_admin_sdk_info = os.environ.get('FIREBASE_ADMIN_SDK_JSON')
    else:
        raise ValueError('FIREBASE_ADMIN_SDK_JSON environment variable not set')

    if 'FIREBASE_DATABASE_NAME' in os.environ:
        logger.error('FIREBASE_DATABASE_NAME environment variable not set')
        firebase_database_name = os.environ.get('FIREBASE_DATABASE_NAME')
    else:
        raise ValueError('FIREBASE_DATABASE_NAME environment variable not set')

    return firebase_admin_sdk_info, firebase_database_name
