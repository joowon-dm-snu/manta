import time
from typing import Any, Dict, Optional, Sequence

from manta_client import Settings

from .manta_history import History


class ProcessStatusAdmin(object):
    pass


EXPERIMENT_PREFIX = "experiment_"


class Experiment(object):
    def __init__(self, settings: Settings = None, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config
        self._settings = settings
        self._settings.update_times()

        self.history = History(self)
        self.history.set_callback(self._history_callback)

        # by set functions
        self._backend = None
        self._observers = None

        # by property & setters from settings
        self._entity = None
        self._project = None
        self._id = settings.experiment_id
        self._name = None
        self._memo = None
        self._tags = None
        self._group = None
        self._job_type = None
        self._start_time = time.time()  # TODO: history start time? settings start time?

        # process admin
        self._process_admin = ProcessStatusAdmin()
        self._setup_from_settings(settings)

    def _setup_from_settings(self, settings):
        """TODO: Need to decide keep tracking value changes at settings instance or at experiment object

        if settings object is frozen, need to keep them in here
        """
        for k, v in settings.__dict__.items():
            try:
                k = k.replace(EXPERIMENT_PREFIX, "")
                setattr(self, f"_{k}", v)
            except KeyError:
                pass

    def set_api(self, api):
        # TODO: merge into set_backend?
        self._api = api

    def set_backend(self, backend):
        self._backend = backend

    def set_observers(self, observer):
        self._observers = observer

    def _history_callback(self, row, step):
        if self._backend and self._backend.interface:
            self._backend.interface.publish_history(row, step)

    @property
    def entity(self) -> str:
        return self._entity

    @property
    def project(self) -> str:
        return self._project

    @property
    def id(self) -> str:
        return self._id

    @property
    def path(self) -> str:
        return "/".join([self.entity, self.project, self.id])

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

    @property
    def dir(self) -> str:
        return self._name

    @property
    def name(self) -> str:
        return self._settings.experiment_name

    @property
    def memo(self) -> str:
        return self._memo

    @memo.setter
    def memo(self, memo: str) -> None:
        self._memo = memo
        # TODO: notify to server memo is changed

    @property
    def group(self) -> str:
        return self._group

    @property
    def job_type(self) -> str:
        return self._job_type

    @property
    def tags(self) -> str:
        return self._tags

    @tags.setter
    def tags(self, tags: Sequence) -> None:
        self._tags = tuple(tags)

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def start_time(self) -> int:
        return self._start_time

    def log(self, data: Dict[str, Any]):
        self.history._row_update(data)
