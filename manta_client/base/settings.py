import copy
import enum
import itertools
import os
import time
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
)

from manta_client.errors import Error  # noqa

settings_defaults = dict(base_url="https://mvp-dev.coxwave.com/api/", mode="online", silent=False)

ENV_PREFIX = "MANTA_"

KEY_MAPPER = {
    "id": "experiment_id",
    "name": "experiment_name",
    "tags": "experiment_tags",
    "notes": "experiment_notes",
}


class Settings(object):
    """Setting

    Settings object is holding parameters for manta-client flow
    Settings can be over-written with multiple phase

    after init process is done, object is frozen and registered
    as global vars
    """

    class UpdateSource(enum.IntEnum):
        BASE: int = 1
        ENTITY: int = 3
        PROJECT: int = 4
        USER: int = 5
        SYSTEM: int = 6
        WORKSPACE: int = 7
        ENV: int = 8
        SETUP: int = 9
        LOGIN: int = 10
        INIT: int = 11
        SETTINGS: int = 12
        ARGS: int = 13

    __frozen = False
    __source_info = dict()

    def __init__(
        self,
        base_url: str = None,
        api_key: str = None,
        mode: str = None,
        entity: str = None,
        team_name: str = None,
        project: str = None,
        experiment_id: str = None,
        experiment_name: str = None,
        experiment_notes: str = None,
        experiment_tags: List[str] = None,
        group: str = None,
        job_type: str = None,
        artfiact_dir: str = None,
        save_code: bool = None,
        config_paths: str = None,
        silent: bool = None,
        _start_time: int = None,
        **kwargs,
    ) -> None:
        """
        mode: online, offline, disable

        """
        kwargs = dict(locals())
        kwargs.pop("self")
        self.__dict__.update({k: None for k in kwargs})

        object.__setattr__(self, "_Settings__frozen", False)
        object.__setattr__(self, "_Settings__source_info", dict())
        self._update(kwargs, _source=self.UpdateSource.SETTINGS)
        self.update_defaults()

    def __copy__(self) -> "Settings":
        s = Settings()
        s.update_settings(self)
        return s

    def duplicate(self) -> "Settings":
        return copy.copy(self)

    def _priority_ok(
        self,
        k: str,
        source: Optional[int],
    ) -> bool:
        key_source: Optional[int] = self.__source_info.get(k)
        if not key_source or not source:
            return True
        if source < key_source:
            return False
        return True

    def _update(self, data: Dict[str, Any] = None, _source: Optional[int] = None, **kwargs: Any) -> None:
        if self.__frozen:
            raise TypeError("Settings object is frozen")

        data = data or dict()
        result = {}
        for check in data, kwargs:
            for k in check.keys():
                if k not in self.__dict__:
                    raise KeyError(k)
                v = check[k]
                if v is None or not self._priority_ok(k, source=_source):
                    continue
                result[k] = v

        for k, v in result.items():
            if isinstance(v, list):
                v = tuple(v)
            self.__dict__[k] = v
            if _source:
                self.__source_info[k] = _source

    def update(self, data: Dict = None, _source=None, **kwargs: Any) -> None:
        self._update(data, _source=_source, **kwargs)

    def update_defaults(self, defaults: Optional[Dict] = None) -> None:
        defaults = defaults or settings_defaults
        self._update(defaults, _source=self.UpdateSource.BASE)

    def update_envs(self, environ: os._Environ) -> None:
        """ """
        # TODO:(kjw) add logic for env key to usable key
        # TODO:(kjw) split tags to tuple
        data = dict()
        for k, v in environ.items():
            if k.startswith(ENV_PREFIX):
                k = k.replace(ENV_PREFIX, "").lower()
                k = KEY_MAPPER.get(k, k)
                data[k] = v
        self._update(data, _source=self.UpdateSource.ENV)

    def update_sys_configs(self) -> None:
        # TODO: (kjw) update configs from manta base dir & curdir
        pass

    def update_settings(self, settings: "Settings") -> None:
        for k in settings._public_keys():
            source = settings.__source_info.get(k)
            self._update({k: settings[k]}, _source=source)

    def update_init(self, kwargs) -> None:
        converted = dict()
        for k, v in kwargs.items():
            converted[KEY_MAPPER.get(k, k)] = v
        self._update(converted, _source=self.UpdateSource.INIT)

    def update_times(self) -> None:
        timestamp = int(time.time() * 1000)
        self._update({"_start_time": timestamp}, _source=self.UpdateSource.INIT)

    def keys(self) -> Iterable[str]:
        return itertools.chain(self._public_keys(), self._property_keys())

    def _public_keys(self) -> Iterator[str]:
        return filter(lambda x: not x.startswith("_Settings__"), self.__dict__)

    def _property_keys(self) -> Generator[str, None, None]:
        return (k for k, v in vars(self).items() if isinstance(v, property))

    def __getitem__(self, k: str) -> Any:
        props = self._property_keys()
        if k in props:
            return getattr(self, k)
        return self.__dict__[k]

    def __setitem__(self, k: str, v: Any) -> None:
        return self.__setattr__(k, v)

    def __setattr__(self, k: str, v: Any) -> None:
        try:
            self._update({k: v}, _source=self.UpdateSource.SETUP)
        except KeyError as e:
            raise AttributeError(str(e))
        object.__setattr__(self, k, v)

    def freeze(self):
        self.__frozen = True

    def is_frozen(self):
        return self.__frozen

    @property
    def _disabled(self) -> bool:
        """
        disable all functionalities include offline saving
        """
        return self.mode == "disable"

    @property
    def _offline(self) -> bool:
        """
        mode == offline will do logging process and save them at local.
        that can be synchronized later if user wants with internet connections
        """
        # be aware settings has disabled property
        return self.mode in ("disable", "offline")

    @property
    def experiemnt_dir(self) -> str:
        return "path/to/somewhere"
