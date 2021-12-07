from typing import Any, Dict, Optional, Sequence, Union

from manta_client import Settings
from manta_client.api import MantaAPI

from . import manta_login, manta_setup
from .backend.backend import Backend
from .libs import globals
from .manta_experiment import Experiment


# TODO: add logger
class _MantaInitiator(object):
    def __init__(self) -> None:
        self._api = None
        self.config = None
        self.settings = None
        self.observers = None

    def _setup_observers(self):
        self.observers = []

    def _setup_configs(self, config_kwargs):
        # setter first, kwargs next
        self.config = dict()
        for data in self.setter._config, config_kwargs:
            if data is None:
                continue
            for k, v in data.items():
                self.config[k] = v

    def _setup_login(self, settings):
        self._api = MantaAPI(settings=settings)
        manta_login.login(api=self._api)
        # TODO: settings.update(api.entity, ...) # update entity or somethings

    def _setup_server_settings(self, settings):
        """
        TODO:
        We think global settings from web can confuse clients
        Discuss later and decide we implement here or not
        """
        pass

    def _setup_logger(self, settings):
        """
        Make default dirs
        Start logging
        """
        pass

    def setup(self, kwargs):
        """Set Settings instance for experiment running

        1. Global setups
        2. Observer setups
        3. Config setups
        4. Create API, Login updates
        5. Client's Server setting updates
        6. init kwargs update
        7. Settings updates
        """
        self.kwargs = kwargs
        self.setter = manta_setup.setup()

        settings: Settings = self.setter.clone_settings()
        settings_param = kwargs.pop("settings", None)
        if settings_param:
            settings.update_settings(settings_param)

        self._setup_observers()

        config_kwargs = kwargs.pop("config", None) or dict()
        self._setup_configs(config_kwargs)

        # TODO: (kjw) online / offline mode
        if not settings._offline:
            self._setup_login(settings=settings)

        # TODO: (kjw) priority of server settings need to be reviewed. (vs init kwargs)
        self._setup_server_settings(settings=settings)

        # working_dir, entity, project, experiment, tags, memo, save_code
        settings.update_init(kwargs)

        # make dirs & init log files
        self._setup_logger(settings)

        self.settings = settings
        self.setter.update(settings)

    def _notify_version(self):
        pass

    def init(self):
        """
        1. init backend
        2. init experiment
        3. start manta_process

        . Update timestamp (server handle it?)

        """
        settings = self.settings

        backend = Backend(api=self._api)
        backend.init_internal_process()

        print("start backend")

        experiment = Experiment(config=self.config, settings=settings)
        experiment.set_backend(backend)
        experiment.set_observers(self.observers)
        print("create experiment")

        experiment.on_init()

        if settings._offline:
            pass

        else:
            self._notify_version()
            # TODO: experiment unique_id set

            # TODO: error handling

            # TODO: cleaning

        # TODO: notify server experiment start

        # TODO: global-vars setting
        globals.set_globals(
            experiment=experiment,
            config=experiment.config,
            meta=experiment.meta,
            summary=experiment.summary,
            log=experiment.log,
            save=experiment.save,
            alarm=experiment.alarm,
            use_artifact=experiment.use_artifact,
            log_artifact=experiment.log_artifact,
        )

        experiment.on_start()
        return experiment


def init(
    artfiact_dir: Optional[str] = None,
    config: Union[Dict, str, None] = None,
    mode: Optional[str] = None,
    entity: Optional[str] = None,
    project: Optional[str] = None,
    id: Optional[str] = None,
    name: Optional[str] = None,
    tags: Optional[Sequence] = None,
    memo: Optional[str] = None,
    save_code=None,
    settings: Union[Settings, Dict[str, Any], None] = None,
) -> Union[Experiment, None]:
    """
    artfiact_dir: not yet
    config: config path
    entity: entity name, cover profile, teams both
    project: project name
    experiment: experiment name
    tags: tags
    memo: long description
    save_code: not yet
    """
    kwargs = dict(locals())

    initiator = _MantaInitiator()
    initiator.setup(kwargs)

    _experiment = initiator.init()
    return _experiment


if __name__ == "__main__":
    init()
