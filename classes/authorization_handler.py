import json
import os
import logging
import sys

from classes.settings_handler import get_settings

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logger.setLevel(LOGLEVEL)
logger.addHandler(stream_handler)


def get_database_reference():
    firebase_admin_sdk_info, firebase_database_name = get_settings()

    if firebase_database_name is None:
        raise ValueError('Firebase database name not available')

    if firebase_admin_sdk_info is None:
        raise ValueError('Firebase credentials not available')

    firebase_admin_sdk_json = json.loads(firebase_admin_sdk_info)
    creds = credentials.Certificate(firebase_admin_sdk_json)

    options_dict = { 'databaseURL': firebase_database_name }
    try:
        firebase_admin.initialize_app(creds, options_dict)
    except ValueError as error:
        print(error)

    database_reference = db.reference('db_root/')
    return database_reference
