import time
from typing import Any, Dict, Optional, Sequence

from manta_client import Settings
from manta_client.base.packet import ExperimentPacket

from .internal.console import ConsoleSync
from .manta_history import History


class ProcessController(object):
    pass


EXPERIMENT_PREFIX = "experiment_"


class Experiment(object):
    def __init__(self, settings: Settings = None, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config
        self._settings = settings
        self._settings.update_times()

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

        # initiated at on_start
        self.history = None
        self.console = None
        self._controller = None
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

    def _setup_from_packet(self, pkt: ExperimentPacket) -> None:
        self._packet = pkt
        self._entity = pkt.entity
        self._project = pkt.project
        # TODO: add config, meta, history ...

    def _setup_packet_offline(self, pkt: ExperimentPacket) -> None:
        self._packet = pkt

    def _as_packet(self, pkt: ExperimentPacket) -> None:
        # TODO: iterate experiment properties for copying
        for k, v in self.__dict__.items():
            # TODO: Add try/except
            pkt[k] = v

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

    def _console_callback(self, name, data):
        if self._backend and self._backend.interface:
            self._backend.interface.publish_console(name, data)

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

    def on_start(self):
        pass

    def on_init(self):
        # TODO: log codes
        self._save_codes()
        # TODO: show exp info
        self._display()

        self._controller = ProcessController()
        self.history = History(self)
        self.history.set_callback(self._history_callback)
        self._console_start()

    def log(self, data: Dict[str, Any]):
        self.history._row_update(data)

    def _save_code(self):
        # TODO: Do this on meta save?
        pass

    def _display(self):
        # TODO: show experiment information
        pass

    def _console_start(self):
        # sync option = REDIRECT, WRAP, OFF
        self.console = ConsoleSync(self)
        self.console.set_callback(self._console_callback)
        self.console.sync(option="redirect")

    def _console_stop(self):
        self.console.stop()
