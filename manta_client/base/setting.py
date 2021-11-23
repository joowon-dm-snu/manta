import copy
import enum
import itertools
import os
from typing import Any, Dict, Generator, Iterable


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

    def __init__(self) -> None:
        super().__init__()

    def __copy__(self) -> "Settings":
        raise NotImplementedError()

    def duplicate(self) -> "Settings":
        return copy.copy(self)

    def _priority_ok(self, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def _update(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    def update(self, item: Dict = None, **kwargs: Any) -> None:
        raise NotImplementedError()

    def update_defaults(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    def update_envs(self, environ: os._Environ) -> None:
        raise NotImplementedError()

    def update_settings(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    def update_login(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    def update_init(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    def keys(self) -> Iterable[str]:
        return itertools.chain(self._public_keys(), self._property_keys())

    def _public_keys(self):
        raise NotImplementedError()

    def _private_keys(self):
        raise NotImplementedError()

    @classmethod
    def _property_keys(cls) -> Generator[str, None, None]:
        return (k for k, v in vars(cls).items() if isinstance(v, property))

    @classmethod
    def _class_keys(cls) -> Generator[str, None, None]:
        return (
            k
            for k, v in vars(cls).items()
            if not k.startswith("_") and not callable(v) and not isinstance(v, property)
        )

    def __getitem__(self, k: str) -> Any:
        props = self._public_keys()
        if k in props:
            return getattr(self, k)
        return self.__dict__[k]

    def __setattr__(self, name: str, value: Any) -> None:
        if name not in self.__dict__:
            raise AttributeError(name)
        if self._Private__frozen:
            raise TypeError("Settings object is frozen")
        object.__setattr__(self, name, value)

    def freeze(self):
        self._Private_frozen = True
    
    def is_frozen(self):
        return self._Private_frozen
