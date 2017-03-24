from flask_httpauth import HTTPBasicAuth
from flask import jsonify, make_response

from configReader import ConfigReader

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):

    if username == ConfigReader.read_config_value('CREDENTIALS', 'username'):
        return ConfigReader.read_config_value('CREDENTIALS', 'password')
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 401)
