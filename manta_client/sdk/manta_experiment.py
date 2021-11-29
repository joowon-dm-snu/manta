from typing import Any, Dict, Optional

from manta_client import Settings


class ProcessStatusController(object):
    pass


class Experiment(object):
    pass

    def __init__(self, settings: Settings = None, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config
        self.settings = settings

    def set_api(self, api):
        # TODO: merge into set_backend?
        self._api = api

    def set_backend(self, backend):
        self._backend = backend

    def set_observers(self, observer):
        self._observers = observer
