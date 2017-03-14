from src.configReader import ConfigReader
from flask_httpauth import HTTPBasicAuth
from flask import jsonify, make_response

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):

    if username == ConfigReader.read_config_value('credentials-config', 'username'):
        return ConfigReader.read_config_value('credentials-config', 'password')
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 401)
