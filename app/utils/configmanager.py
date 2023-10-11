from configparser import ConfigParser

from utils.singleton_mixin import SingletonMixin


class ConfigManager(SingletonMixin):
    config_parser = ConfigParser()
    file = ''

    def __init__(self, file='settings.ini'):
        self.config_parser.read(file, encoding="utf8")
        self.file = file
        print(f'ConfigManager: "{self.file}" Initialized with ID: {id(self)}')

    def __repr__(self) -> str:
        return f"<ConfigManager: {self.file}>"

    @property
    def config(self):
        return self.config_parser

    def _write_config(self):
        with open(self.file, 'w', encoding="utf8") as configfile:
            self.config_parser.write(configfile)

    def update_field(self, section, field, value):
        self.config_parser.set(section, field, value)
        self._write_config()

    def delete_field(self, section, field):
        self.config_parser.remove_option(section, field)
        self._write_config()
