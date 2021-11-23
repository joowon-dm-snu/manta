import os
import pytest
import tempfile

import manta_client as mc


def update_callback(d):
    def func(key=None, val=None, data=None):
        if data:
            d.update(data)
        if key:
            d[key] = val

    return func


@pytest.fixture()
def callback_dict():
    return {}


@pytest.fixture()
def callback_func(callback_dict):
    return update_callback(callback_dict)


@pytest.fixture()
def config(callback_func):
    s = mc.Config()
    s.set_callback(callback_func)
    return s


def test_attribute_compatible(callback_dict, config):
    config.attribute = 0
    assert dict(config) == dict(attribute=0)
    assert callback_dict == dict(config)


def test_update(callback_dict, config):
    config.update(dict(some=8))
    assert dict(config) == dict(some=8)
    config.update(dict(thing=4))
    assert dict(config) == dict(some=8, thing=4)
    assert callback_dict == dict(config)


def test_dict_functions(config):
    target = dict(some=8, thing=4)
    config.update(target)
    assert config.keys() == target.keys()
    assert config.values() == target.values()
    assert config.items() == target


def test_value_sanitized(config):
    target = dict(some=dict(sanitized="ab-"), thing=4)
    config.update(target)
    assert config.some.sanitized == "ab"


def test_auto_config_default():
    tempdir = tempfile.NamedTemporaryFile()
    yaml_path = os.path.join(tempdir, "config_default.yaml")
    yaml_dict = {"some": {"value": 1}, "thing": {"value": 2}}
    mc.util.save_yaml(yaml_path, yaml_dict)

    config = mc.Config()
    tempdir.close()
    assert dict(config) == dict(some=1, thing=2)
