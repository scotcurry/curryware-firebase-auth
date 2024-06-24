import time
import requests
from classes import authorization_handler


def get_oauth_info_from_firebase():
    oauth_settings_path = 'oauth_info/'

    database_reference = authorization_handler.get_database_reference()
    oauth_path_reference = database_reference.child(oauth_settings_path)
    oauth_token = oauth_path_reference.get()

    return oauth_token


def check_if_auth_token_is_valid(oauth_token):
    current_unix_timestamp = int(time.time())
    valid_token_time = current_unix_timestamp + 3599
    last_token_update = oauth_token.last_token_update
    if last_token_update < valid_token_time:
        return True


def get_new_oauth_token_from_refresh_token(oauth_token):
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
        return new_oauth_token, new_refresh_token


def update_new_token_info(new_oauth_token, new_refresh_token):
    database_reference = authorization_handler.get_database_reference()
    oauth_node = database_reference.child('oauth_info')
    current_unix_timestamp = int(time.time())
    new_oauth_info_dict = {'auth_token': new_oauth_token, 'refresh_token':
        new_refresh_token, 'last_token_update': current_unix_timestamp}
    new_reference = oauth_node.update(new_oauth_info_dict)
    return new_reference
