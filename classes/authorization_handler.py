import json
import os
import logging
import sys

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

    if firebase_admin_sdk_info is None:
        logger.error('Firebase sdk info not set')
        raise ValueError('Firebase credentials not available')

    firebase_admin_sdk_json = json.loads(firebase_admin_sdk_info)
    creds = credentials.Certificate(firebase_admin_sdk_json)

    options_dict = { 'databaseURL': firebase_database_name }
    try:
        firebase_admin.initialize_app(creds, options_dict)
    except ValueError as error:
        logger.warning(error.args[0])

    database_reference = db.reference('db_root/')
    return database_reference
