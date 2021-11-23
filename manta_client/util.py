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
        raise Error("Couldn't read yaml file: %s" % path)
    except UnicodeDecodeError:
        print("wrong encoding")
    return result


def read_config_yaml(path: Union[str, Path], keyname: str = "value") -> Dict:
    # TODO: (kjw) this process can be efficient but think this is not a time-consuming issue
    result = dict()
    for k, v in read_yaml(path).items():
        result[k] = v[keyname]
    return result


def save_yaml(path: Union[str, Path], info: Dict) -> None:
    mkdir(Path(path).parent)

    with open(path, "w") as f:
        yaml.dump(info, f)


def to_dict(params):
    if isinstance(params, dict):
        return params
    elif isinstance(params, argparse.Namespace):
        pass
    elif isinstance(params, argparse.ArgumentParser):
        pass
    else:
        try:
            params = params.items()
        except Exception as e:
            print(e)
            raise AttributeError()


def json_value_sanitize(value):
    return value
