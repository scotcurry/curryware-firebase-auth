import json
import logging

from classes.settings_handler import get_settings

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s '
          'dd.version=%(dd.version)s '
          'dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')

logging.basicConfig(format=FORMAT)
logger = logging.getLogger('curryware-firebase-auth')
logger.level = logging.DEBUG


def get_database_reference():
    firebase_admin_sdk_info, firebase_database_name = get_settings()

    if firebase_database_name is None:
        logger.error('Firebase database name not set')
        raise ValueError('Firebase database name not available')
    else:
        logger.info('authorization_handler - '
                    'DB Name: {}'.format(firebase_database_name))

    if firebase_admin_sdk_info is None:
        logger.error('Firebase sdk info not set')
        raise ValueError('Firebase credentials not available')
    else:
        firebase_admin_sdk_info_log = firebase_admin_sdk_info
        logger.info('authorization_handler - {}'.format(firebase_admin_sdk_info_log))

    try:
        # Because the certificate has new line characters in it, it will throw an error
        # we need to set the strict flag to overcome this.
        firebase_admin_sdk_json = json.loads(firebase_admin_sdk_info, strict=False)
        creds = credentials.Certificate(firebase_admin_sdk_json)
    except ValueError as error:
        logger.error('Error parsing Firebase credentials: {}'.format(error.args[0]))

    options_dict = {'databaseURL': firebase_database_name}
    try:
        firebase_admin.initialize_app(creds, options_dict)
    except ValueError as error:
        logger.error('Error initializing Firebase app')

    database_reference = db.reference('db_root/')
    return database_reference
