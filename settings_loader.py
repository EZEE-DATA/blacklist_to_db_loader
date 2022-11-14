from settings.settings import get_list_of_settings, environment_variable_name
from os import environ


class SettingsFile:
    """
    Implement SettingsFile class- a set of methods
    to get and store settings information
    """

    def __init__(self, settings_file_path: str) -> object:
        self.__settings_file_path = settings_file_path
        self.__settings = None
        self.get_settings_from_file()

    def get_settings_from_file(self) -> str:
        """
        :return: settings, or None if not available
        """
        with open(self.__settings_file_path, 'r') as settings_file:
            settings = settings_file.readline().replace('\n', '')
        if not settings or len(settings) < 1:
            raise ValueError('Provided file has no settings!')
        self.settings = settings
        return self.settings

    @property
    def settings(self) -> str:
        assert isinstance(self.__settings, object)
        return self.__settings

    @settings.setter
    def settings(self, value: str):
        self.__settings = value


def load_variables_to_environment(settings_directory: str) -> list[environment_variable_name]:
    """
    Load variables to environment and return list of environment variables names
    :rtype: list[environment_variable_name]
    """
    params = get_list_of_settings(settings_directory)
    for param in params:
        environ[param] = SettingsFile(settings_directory + '/' + param + '.list').settings
    return params
