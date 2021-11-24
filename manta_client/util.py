import argparse
import os
import yaml
from pathlib import Path
from typing import Any, Dict, Union

from manta_client.errors import Error


def mkdir(path: Union[str, Path], exist_ok: bool = True) -> bool:
    try:
        os.makedirs(path, exist_ok=exist_ok)
        return True
    except OSError as exc:
        print(exc)
        return False


def read_yaml(path: Union[str, Path], encoding="utf-8") -> Dict:
    result = dict()

    try:
        with open(path, encoding=encoding) as f:
            for param in yaml.load_all(f, Loader=yaml.FullLoader):
                result.update(param)
    except OSError:
        print("Couldn't read yaml file: %s" % path)
    except UnicodeDecodeError:
        print("wrong encoding")
    return result


def read_config_yaml(
    path: Union[str, Path] = None, data: Dict = None, keyname: str = "value"
) -> Dict:
    if path and data is None:
        data = read_yaml(path)
    elif path is None and data:
        pass
    else:
        raise AttributeError()

    result = dict()
    for k, v in data.items():
        if isinstance(v, Dict) and keyname not in v:
            result[k] = read_config_yaml(data=v)
        else:
            result[k] = v[keyname]
    return result


def save_yaml(path: Union[str, Path], info: Dict) -> None:
    if mkdir(Path(path).parent):
        with open(path, "w") as f:
            yaml.dump(info, f)
    else:
        # TODO: (kjw) will be changed for error handling
        print("mkdir failed")


def to_dict(params):
    if isinstance(params, Dict):
        return params
    elif isinstance(params, argparse.Namespace):
        return vars(params)
    else:
        try:
            params = params.items()
        except Exception as e:
            print(e)
            raise AttributeError()


def json_value_sanitize(value):
    # TODO: tensor values will be change to float here
    return value
