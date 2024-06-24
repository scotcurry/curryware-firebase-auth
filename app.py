from flask import Flask
from classes.oauth_token_handler import (get_oauth_info_from_firebase,
                                         check_if_auth_token_is_valid,
                                         get_new_oauth_token_from_refresh_token)

app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index_page():
    return "currware-firebase-auth index page"


@app.route('/get_oauth_token', methods=['GET'])
def get_oauth_token():

    try:
        oauth_info = get_oauth_info_from_firebase()
    except ValueError as exception:
        return exception.args[0]

    if check_if_auth_token_is_valid(oauth_info):
        return oauth_info['access_token']

    new_oauth_info = get_new_oauth_token_from_refresh_token(oauth_info)

    return new_oauth_info['access_token']
