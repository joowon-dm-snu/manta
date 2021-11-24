class Error(Exception):
    def __init__(self, message):
        super(Error, self).__init__(message)
        self.message = message


class ConfigError(Error):
    pass


class SettingError(Error):
    pass
