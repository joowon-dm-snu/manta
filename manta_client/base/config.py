from typing import Any, Dict, Tuple  # , Union

# from pathlib import Path

import manta_client.util as util
from manta_client.errors import ConfigError


# TODO: (kjw) need to think depth. ex) config.param1.param2 or config.param1.param2.params3...
class Config(object):
    """Config

    Config object is used to save all hyperparams.
    Config can be over-written with 2 stages.
      - project config
      - user control

    Examples:
        Basic
        ```python
        mc.config.param = 0
        ```

        Working like nested dict
        ```python
        mc.config.nested.param1 = 1
        mc.config['nested']['param2'] = 2
        ```

        Input by initiation phase
        ```python
        mc.init(config={'param1': 1, 'param2': 2})
        ```

        From ArgumentParser
        ```python
        parser = argparse.ArgumentParser()
        parser.add_argument('--something', type=int, default=123)
        args = parser.parse_args()

        mc.config.something = 0
        mc.config.update(args)
        ```

        From argparse.Namespace
        ```python
        args = argparse.Namespace()
        args.something = 123

        mc.config.something = 0
        mc.config.update(args)
        ```

        From yaml
        ```python
        mc.config.update_yaml(yaml_path)
        ```
    """

    def __init__(self) -> None:
        object.__setattr__(self, "_items", dict())
        object.__setattr__(self, "_callback", None)
        object.__setattr__(self, "_settings", None)

        self._load_defaults()

    def _load_defaults(self):
        conf_dict = util.read_config_yaml("config_defaults.yaml")
        if conf_dict is not None:
            self.update(conf_dict)

    def _assert_dict_values(self, v: Any) -> None:
        raise NotImplementedError()

    def _sanitize(self, k: str, v: Any) -> Tuple:
        k = k.rstrip("_|-")
        v = util.json_value_sanitize(v)
        return k, v

    def _sanitize_dict(self, config_dict: Dict) -> Dict:
        sanitized = {}
        self._assert_dict_values(config_dict)

        for k, v in config_dict.items():
            k, v = self._sanitize(k, v)
            sanitized[k] = v
        return sanitized

    def __setitem__(self, k, v):
        self._assert_dict_values(v)
        v = self._sanitize(k)
        self._items[k] = v

        print("config __setitem__ {} = {} - {}".format(k, v, self._callback))
        if self._callback:
            self._callback(key=k, val=v)

    def __setattr__(self, k, v):
        return self.__setitem__(k, v)

    def update(self, param):
        if isinstance(param, str):
            data = util.read_config_yaml(param)

        # TODO: (kjw): try-except usage
        data = util.to_dict(param)
        data = self._sanitize_dict(data)
        self._items.update(data)

        if self._callback:
            self._callback(data=data)

    def __getitem__(self, k):
        return self._items[k]

    def __getattr__(self, k):
        return self.__getitem__(k)

    def __contains__(self, k):
        return k in self._items

    def keys(self):
        return [k for k in self._items.keys() if not k.startswith("_")]

    def values(self):
        return [v for k, v in self._items.items() if not k.startswith("_")]

    def items(self):
        return [(k, v) for k, v in self._items.items() if not k.startswith("_")]

    def set_callback(self, fn):
        self._callback = fn

    def get(self, *args):
        return self._items.get(*args)

    def as_dict(self):
        return self._items
