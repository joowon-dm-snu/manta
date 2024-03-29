import argparse
import os
import queue
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import shortuuid
import yaml

from manta_client.errors import Error


def mkdir(path: Union[str, Path], exist_ok: bool = True) -> bool:
    try:
        os.makedirs(path, exist_ok=exist_ok)
        return True
    except OSError as exc:
        print(exc)
        return False


def parent_makedirs(path: Union[str, Path], exist_ok: bool = True) -> bool:
    path = Path(path).parent
    mkdir(path)


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


def read_config_yaml(path: Union[str, Path] = None, data: Dict = None, keyname: str = "value") -> Dict:
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


def generate_id(length=10):
    run_gen = shortuuid.ShortUUID(alphabet=list("0123456789abcdefghijklmnopqrstuvwxyz"))
    return run_gen.random(length)


def read_many_from_queue(q: queue.Queue, max_items: int, timeout: int) -> List[Tuple]:
    try:
        item = q.get(True, timeout)
    except queue.Empty:
        return []
    items = [item]
    for i in range(max_items):
        try:
            item = q.get_nowait()
        except queue.Empty:
            return items
        items.append(item)
    return items
