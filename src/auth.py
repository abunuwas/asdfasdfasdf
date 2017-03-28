from flask_httpauth import HTTPBasicAuth
from flask import jsonify, make_response

from config_reader import ConfigReader

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    """
    Returns the password for the username parameter from the config file
    :param username: The current username supplied in the auth header
    :return: Password associated with the user
    """
    if username == ConfigReader.read_config_value('CREDENTIALS', 'username'):
        return ConfigReader.read_config_value('CREDENTIALS', 'password')
    return None


@auth.error_handler
def unauthorized():
    """
    Handler for unauthorized errors
    :return: 401 unauthorized
    """
    return make_response(jsonify({'message': 'Unauthorized access'}), 401)
