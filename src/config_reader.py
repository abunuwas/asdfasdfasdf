import configparser
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class ConfigReader:

    @staticmethod
    def read_config_value(settings, key):
        """
        Read in a value from the application configuration file (application.config)
        :param settings: The config settings area within the file
        :param key: The specific key to be read
        :return: The value associated with the key in the config file
        """
        config_parser = configparser.RawConfigParser()
        config_file_path = os.path.join(basedir[:-3], os.path.join('config', 'application.config'))
        config_parser.read(config_file_path)

        return config_parser.get(settings, key)

