import configparser
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class ConfigReader:

    @staticmethod
    def read_config_value(settings, key):

        config_parser = configparser.RawConfigParser()
        config_file_path = os.path.join(basedir[:-3], os.path.join('config', 'application.config'))
        config_parser.read(config_file_path)

        return config_parser.get(settings, key)

