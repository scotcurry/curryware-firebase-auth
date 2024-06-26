import os
import sys
import logging
from flask import Flask
from classes.oauth_token_handler import (get_oauth_info_from_firebase,
                                         check_if_auth_token_is_valid,
                                         get_new_oauth_token_from_refresh_token)

app = Flask(__name__)

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logger.setLevel(LOGLEVEL)
logger.addHandler(stream_handler)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index_page():
    return "currware-firebase-auth index page"


@app.route('/get_oauth_token', methods=['GET'])
def get_oauth_token():
    logger.info('/get_oauth_token called')
    try:
        oauth_info = get_oauth_info_from_firebase()
        logger.info('Successfully fetched oauth info')
    except ValueError as exception:
        logger.error(exception.args[0])
        return exception.args[0]

    if check_if_auth_token_is_valid(oauth_info):
        logger.info('Successfully fetched valid oauth info')
        oauth_token = oauth_info['auth_token']
        return oauth_token

    try:
        new_oauth_token, new_refresh_token = get_new_oauth_token_from_refresh_token(oauth_info)
        logger.info('Successfully fetched new oauth info')
    except ValueError as exception:
        logger.error(exception.args[0])

    return new_oauth_token
