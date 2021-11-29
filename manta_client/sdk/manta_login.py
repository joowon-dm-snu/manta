from manta_client import Settings
from manta_client.api import MantaAPI


class _MantaLogin(object):
    def __init__(self, silent: bool = False) -> None:
        self._api_key = None
        self._silent = silent

    def display(self):
        pass

    def setup(self, kwargs):
        pass

    def validate_api_key(self, key):
        pass

    def prompt_api_key(self):
        """request user to put api key on terminal"""
        pass

    def login(self):
        pass


def login(
    api_key: str = None, base_url: str = None, settings: Settings = None, api: MantaAPI = None, silent: bool = None
):
    kwargs = dict(locals())

    silent = kwargs.pop("silent", None)
    _login = _MantaLogin(silent=silent)
    _login.setup(kwargs)

    logged_in = _login.login()

    key = kwargs.get("key")
    _login.validate_api_key(key)

    if logged_in:
        return logged_in

    if key is None:
        _login.prompt_api_key()

    return _login._api_key or False
