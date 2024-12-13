import os
import sys
import time
import logging
import requests

from classes import authorization_handler
from classes.authorization_handler import get_database_reference

#if 'RUNNING_IN_FUNCTION' not in os.environ:
FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '- %(message)s')
# else:
#     FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
#               '[dd.service=%(dd.service)s dd.env=%(dd.env)s '
#               'dd.version=%(dd.version)s '
#               'dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
#               '- %(message)s')

logging.basicConfig(format=FORMAT)
logger = logging.getLogger('curryware-firebase-auth-oauth-token-handler')
logger.level = logging.DEBUG


def get_oauth_info_from_firebase():

    oauth_settings_path = 'oauth_info/'

    try:
        database_reference = authorization_handler.get_database_reference()
        database_reference_path = database_reference.path
        logger.info(f'Database reference: {database_reference_path}')
    except ValueError as exception:
        logger.error("Error retrieving oauth info from firebase")
        logger.error(exception.args[0])
        return 'Error'

    try:
        oauth_path_reference = database_reference.child(oauth_settings_path)
        logger.info(f'OAuth path reference: {oauth_path_reference.path}')
    except ValueError as exception:
        logger.error(exception.args[0])
        return 'Error'

    try:
        logger.info('Getting oauth info from firebase')
        oauth_token = oauth_path_reference.get()
        auth_token = oauth_token['auth_token']
        refresh_token = oauth_token['refresh_token']
        last_update_time = oauth_token['last_token_update']
        auth_token_stub = auth_token[0:5]
        refresh_token_stub = refresh_token[0:5]
        logger.debug(f'OAuth token: {auth_token_stub}')
        logger.debug(f'Refresh token: {refresh_token_stub}')
        logger.debug(f'Last update time: {last_update_time}')
        return oauth_token
    except Exception as exception:
        logger.error(exception.args[0])
        return 'Error'


def check_if_auth_token_is_valid(oauth_token):
    # Get the current time and add an hour.  If the last update was in the past hour, i.e.
    # the auth_token i
    logger.info('Checking if auth token is valid')
    current_unix_timestamp = int(time.time())
    last_token_update = oauth_token['last_token_update']
    valid_token_time = last_token_update + 3599
    if current_unix_timestamp > valid_token_time:
        logger.info(f'Last Token Update - Token still valid')
        logger.info(f'Current Time: {current_unix_timestamp}, Valid Token Time: '
                    f'{valid_token_time}')
        return False

    logger.info(f'Last Token Update - New Token Required')
    return True


def get_new_oauth_token_from_refresh_token(oauth_token):
    logger.info(f'Getting New OAuth Token from Refresh Token')
    request_data = {'client_id': oauth_token['clientID'],
                    'client_secret': oauth_token['clientSecret'],
                    'redirect_uri': oauth_token['redirect_url'],
                    'refresh_token': oauth_token['refresh_token'],
                    'grant_type': 'refresh_token'}

    refresh_token_endpoint = oauth_token['authority'] + oauth_token['token_endpoint']
    refresh_token = requests.post(refresh_token_endpoint, data=request_data, timeout=5)
    if refresh_token.status_code == 200:
        refresh_token_json = refresh_token.json()
        new_oauth_token = refresh_token_json['access_token']
        new_refresh_token = refresh_token_json['refresh_token']
        update_new_token_info(new_oauth_token, new_refresh_token)
        logger.info(f'Successfully got new OAuth token')
        return new_oauth_token, new_refresh_token


def update_new_token_info(new_oauth_token, new_refresh_token):
    logger.info(f'Updating Token Information')
    database_reference = authorization_handler.get_database_reference()
    oauth_node = database_reference.child('oauth_info')
    current_unix_timestamp = int(time.time())
    new_oauth_info_dict = {'auth_token': new_oauth_token, 'refresh_token':
        new_refresh_token, 'last_token_update': current_unix_timestamp}
    new_reference = oauth_node.update(new_oauth_info_dict)
    return new_reference
