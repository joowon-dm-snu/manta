import copy
import os
import pytest

import manta_client as mc
from manta_client import Settings
from manta_client.errors import SettingError


def test_initial_defaults():
    s = Settings()
    s.init()
    assert s.base_url == "https://api.coxwave.com"


def test_attrib_get_set():
    s = Settings()
    s.base_url = "test1"
    assert s.base_url == "test1"
    s["base_url"] = "test2"
    assert s["base_url"] == "test2"


def test_attrib_get_invalid_key():
    s = Settings()
    with pytest.raises(AttributeError):
        s.invalid_key
    with pytest.raises(AttributeError):
        s["invalid_key"]


def test_attrib_set_invalid_key():
    s = Settings()
    with pytest.raises(AttributeError):
        s.invalid_key = "error"
    with pytest.raises(AttributeError):
        s["invalid_key"] = "error"


def test_update_dict():
    s = Settings()
    s.update(dict(base_url="something"))
    assert s.base_url == "something"


def test_update_kwargs():
    s = Settings()
    s.update(base_url="something")
    assert s.base_url == "something"


def test_update_both():
    s = Settings()
    s.update(dict(base_url="something"), project="nothing")
    assert s.base_url == "something"
    assert s.project == "nothing"


def test_ignore_globs():
    s = Settings()
    s.setdefaults()
    assert s.ignore_globs == ()


def test_ignore_globs_explicit():
    s = Settings(ignore_globs=["foo"])
    s.setdefaults()
    assert s.ignore_globs == ("foo",)


def test_ignore_globs_env():
    s = Settings()
    s._apply_environ({"manta_IGNORE_GLOBS": "foo,bar"})
    s.setdefaults()
    assert s.ignore_globs == (
        "foo",
        "bar",
    )


def test_update_defaults():
    s = Settings()
    s.update_envs({"base_url": "update_defaults"})
    assert s.base_url == "update_defaults"


def test_update_envs():
    s = Settings()
    s.update_envs({"MANTA_BASE_URL": "update_envs"})
    assert s.base_url == "update_envs"


def test_copy():
    s = Settings()
    s.update(base_url="changed")
    s2 = copy.copy(s)
    assert s2.base_url == "changed"
    s.update(base_url="notchanged")
    assert s.base_url == "notchanged"
    assert s2.base_url == "changed"


def test_invalid_dict():
    s = Settings()
    with pytest.raises(KeyError):
        s.update(dict(invalid="test"))


def test_invalid_kwargs():
    s = Settings()
    with pytest.raises(KeyError):
        s.update(invalid="test")


def test_no_update_for_invalid():
    s = Settings()
    with pytest.raises(KeyError):
        s.update(dict(project="noop0"), invalid="test")
    assert s.project != "noop0"
    with pytest.raises(KeyError):
        s.update(entity="noop1", project="noop2", invalid="test")
    assert s.entity != "noop1"
    assert s.project != "noop2"


def test_freeze():
    s = Settings()
    s.project = "no_change"
    assert s.project == "no_change"

    s.freeze()
    with pytest.raises(TypeError):
        s.project = "try"
    assert s.project == "no_change"

    with pytest.raises(TypeError):
        s.update(project="badprojo2")
    assert s.project == "no_change"

    c = copy.copy(s)
    assert c.project == "no_change"
    c.project = "changed"
    assert c.project == "changed"


# def test_bad_choice():
#     s = Settings()
#     with pytest.raises(KeyError):
#         s.mode = "goodprojo"
#     with pytest.raises(KeyError):
#         s.update(mode="badpro")


def test_prio_update_ok():
    s = Settings()
    s.update(project="pizza", _source=s.UpdateSource.ENTITY)
    assert s.project == "pizza"
    s.update(project="pizza2", _source=s.UpdateSource.PROJECT)
    assert s.project == "pizza2"


def test_prio_update_ignore():
    s = Settings()
    s.update(project="pizza", _source=s.UpdateSource.PROJECT)
    assert s.project == "pizza"
    s.update(project="pizza2", _source=s.UpdateSource.ENTITY)
    assert s.project == "pizza"


def test_validate_base_url():
    s = Settings()
    with pytest.raises(ValueError):
        s.update(base_url="https://coxwave.app")
    s.update(base_url="https://api.coxwave.app")
    assert s.base_url == "https://api.coxwave.app"


def test_preprocess_base_url():
    s = Settings()
    s.update(base_url="http://host.com")
    assert s.base_url == "http://host.com"
    s.update(base_url="http://host.com/")
    assert s.base_url == "http://host.com"
    s.update(base_url="http://host.com///")
    assert s.base_url == "http://host.com"
    s.update(base_url="//http://host.com//")
    assert s.base_url == "//http://host.com"
