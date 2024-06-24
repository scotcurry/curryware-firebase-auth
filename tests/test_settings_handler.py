from unittest import TestCase
from classes.settings_handler import get_settings
from classes.authorization_handler import get_database_reference
from classes.oauth_token_handler import (get_oauth_info_from_firebase,
                                         get_new_oauth_token_from_refresh_token)


class TestSettingsHandler(TestCase):

    def test_get_settings(self):
        firebase_admin_sdk_info, firebase_database_name = get_settings()
        assert (firebase_admin_sdk_info is not None) and (firebase_database_name is not None)

    def test_get_authorization_token(self):
        auth_token = get_database_reference()
        assert auth_token.key == 'db_root'

    def test_oauth_token_handler(self):
        oauth_token = get_oauth_info_from_firebase()
        assert oauth_token is not None

    def test_check_if_refresh_token_is_needed(self):
        oauth_token = get_oauth_info_from_firebase()
        assert oauth_token is not None

    def test_get_new_oauth_token_from_refresh_token(self):
        oauth_token = get_oauth_info_from_firebase()
        new_oauth_token, refresh_token = get_new_oauth_token_from_refresh_token(
            oauth_token)
        assert (new_oauth_token is not None) and (refresh_token is not None)
