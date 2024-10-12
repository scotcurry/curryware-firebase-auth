import os
import logging


def get_settings():

    if 'RUNNING_IN_FUNCTION' not in os.environ:
        FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
                  '- %(message)s')
    else:
        FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
                  '[dd.service=%(dd.service)s dd.env=%(dd.env)s '
                  'dd.version=%(dd.version)s '
                  'dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
                  '- %(message)s')

    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('curryware-firebase-auth-settings-handler')
    logger.level = logging.DEBUG

    if 'FIREBASE_ADMIN_SDK_JSON' in os.environ:
        firebase_admin_sdk_info= os.environ.get('FIREBASE_ADMIN_SDK_JSON')
        firebase_admin_sdk_info_to_log = firebase_admin_sdk_info[0:10] + '...'
        logger.info(firebase_admin_sdk_info_to_log)
    else:
        logger.error('FIREBASE_ADMIN_SDK_JSON is not set')
        raise ValueError('FIREBASE_ADMIN_SDK_JSON environment variable not set')

    if 'FIREBASE_DATABASE_NAME' in os.environ:
        firebase_database_name = os.environ.get('FIREBASE_DATABASE_NAME')
        firebase_database_name_to_log = firebase_database_name[0:10] + '...'
        logger.info(firebase_database_name_to_log)
    else:
        logger.error('FIREBASE_DATABASE_NAME is not set')
        raise ValueError('FIREBASE_DATABASE_NAME environment variable not set')

    return firebase_admin_sdk_info, firebase_database_name
