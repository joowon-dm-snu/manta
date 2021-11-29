import os

from manta_client import Settings
from manta_client.util import read_config_yaml


class _MantaSetupInstance(object):
    """Singleton instance"""

    def __init__(self, settings=None, environ=None) -> None:
        self._settings = None
        self._environ = environ or dict(os.environ)
        self._config = dict()

        self._setup_settings()
        self._setup_configs()

    def _setup_settings(self, settings=None):
        s = Settings()
        s.update_sys_configs()
        s.update_envs(self._environ)
        if settings:
            s.update_settings(settings)

        self._settings = s

    def _setup_configs(self):
        # update user's custom conf files except basedir or curdir configs
        # TODO: show warning, values can be overwritten
        if self._settings.config_paths:
            config_paths = self._settings.config_paths.split(",")
            for path in config_paths:
                config = read_config_yaml(path) or dict()
                self._config.update(config)

    def update(self, settings: Settings = None):
        if settings:
            s = self.clone_settings()
            s.update_settings(settings=settings)
            self._settings = s

    def clone_settings(self):
        return self._settings.duplicate()


class _MantaGlobalSetup(object):
    _instance = None

    def __init__(self, settings=None):
        if _MantaGlobalSetup._instance is not None:
            _MantaGlobalSetup._instance.update(settings=settings)
        else:
            _MantaGlobalSetup._instance = _MantaSetupInstance(settings=settings)

    def __getattr__(self, name):
        return getattr(self._instance, name)

    def __setattr__(self, name):
        # TODO: do we need this ?
        return setattr(self._instance, name)


def setup(settings=None):
    gs = _MantaGlobalSetup(settings=settings)
    return gs
