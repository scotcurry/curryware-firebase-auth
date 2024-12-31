import json
import logging
from flask import Flask, request
from classes.oauth_token_handler import (get_oauth_info_from_firebase,
                                         check_if_auth_token_is_valid,
                                         get_new_oauth_token_from_refresh_token)

app = Flask(__name__)

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
logger = logging.getLogger('curryware-firebase-auth - app - ')
logger.level = logging.DEBUG


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index_page():
    logger.info('index page called')
    html_head = ('<html><head><title>Curryware Firebase Auth</title></head>'
                 '<body><p><a href="/get_oauth_token">Get OAuth Token</a></p></body>'
                 '</html>')
    return html_head


@app.route('/get_oauth_token', methods=['GET'])
def get_oauth_token():
    logger.info('/get_oauth_token called')
    headers = request.headers
    for key, value in headers.items():
        logger.info(f'{key}: {value}')

    try:
        oauth_info = get_oauth_info_from_firebase()
        logger.info('Successfully fetched oauth info')
    except ValueError as exception:
        logger.error('Error fetching oauth info')
        logger.error(exception.args[0])
        return 'Failed to fetch oauth info', 500

    if check_if_auth_token_is_valid(oauth_info):
        logger.info('Successfully fetched valid oauth info')
        oauth_token = oauth_info['auth_token']
        last_token_update = oauth_info['last_token_update']
        auth_token_dict = {'oauth_token': oauth_token, 'last_token_update': last_token_update}
        auth_token_json = json.dumps(auth_token_dict)
        return auth_token_json

    try:
        new_oauth_token, new_refresh_token = (
            get_new_oauth_token_from_refresh_token(oauth_info))
        logger.info('Successfully fetched new oauth info')
        auth_token_json = {'oauth_token': new_oauth_token}
    except ValueError as exception:
        logger.error(exception.args[0])

    return auth_token_json
