import argparse
import os
import pytest

import manta_client as mc


@pytest.fixture()
def config():
    return mc.Config()


def test_attribute_compatible(config):
    config.attribute = 0
    assert dict(config) == dict(attribute=0)


def test_update(config):
    config.update(dict(some=8))
    assert dict(config) == dict(some=8)
    config.update(dict(thing=4))
    assert dict(config) == dict(some=8, thing=4)


def test_update_from_argparse(config):
    args = argparse.Namespace()
    args.something = 123
    config.update(args)

    assert config.something == 123


def test_update_from_yaml(config):
    yaml_path = os.path.join("user_config.yaml")
    yaml_dict = {"some": {"key": {"value": 99}}, "thing": {"value": 999}}
    mc.util.save_yaml(yaml_path, yaml_dict)

    config.update(yaml_path)
    assert dict(config) == dict(some=dict(key=99), thing=999)
    os.remove(yaml_path)


def test_update_nested_input(config):
    nested_dict = {"key1": {"key2": {"value": 123}}}
    config.update(nested_dict)
    assert config["key1"]["key2"]["value"] == 123


def test_dict_functions(config):
    target = dict(some=8, thing=4)
    config.update(target)
    assert "some" in config
    assert config.keys() == list(target.keys())
    assert config.values() == list(target.values())
    assert config.items() == list(target.items())


# TODO: Does config need key sanitized?
def test_key_sanitized(config):
    target = dict(some=dict(sanitized_="ab-"), thing=4)
    config.update(target)
    assert config.some["sanitized"] == "ab-"


# TODO: Does config need value sanitized for tensors?
# def test_value_sanitized(config):
#     target = dict(some=dict(sanitized_="ab-"), thing=4)
#     config.update(target)
#     assert config.some["sanitized"] == "ab-"


def test_auto_config_default():
    yaml_path = os.path.join("config_defaults.yaml")
    yaml_dict = {"some": {"value": 1}, "thing": {"value": 2}}
    mc.util.save_yaml(yaml_path, yaml_dict)

    config = mc.Config()

    assert dict(config) == dict(some=1, thing=2)
    os.remove(yaml_path)
