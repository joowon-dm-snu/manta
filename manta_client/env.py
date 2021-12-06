import os
import sys
from distutils.util import strtobool

# env keys
HTTP_TIMEOUT = "MANTA_HTTP_TIMEOUT"
BASE_DIR = "MANTA_BASE_DIR"
CACHE_DIR = "MANTA_CACHE_DIR"
API_KEY = "MANTA_API_KEY"
MANTA_DIR = "MANTA_DIR"


def env_as_bool(key, env=None):
    env = env or os.environ
    val = env.get(key, None)
    try:
        val = bool(strtobool(val))
        return val
    except (AttributeError, ValueError):
        return False


def get_http_timeout(default=10, env=None):
    env = env or os.environ
    val = int(env.get(HTTP_TIMEOUT, default))
    return val


def get_manta_sysdir(env=None):
    default_dir = os.path.expanduser(os.path.join("~", ".manta"))
    env = env or os.environ
    path = env.get(BASE_DIR, default_dir)
    return path


def get_manta_cache_dir(env=None):
    default_dir = os.path.expanduser(os.path.join("~", ".cache", "manta"))
    env = env or os.environ
    path = env.get(CACHE_DIR, default_dir)
    return path


def get_manta_dir(env=None):
    if env is None:
        env = os.environ
    return env.get(MANTA_DIR, None)


def get_api_key(host, env_first=True):
    """get api key from manta sysdir or env-vars

    ~/.manta/configuration.yaml
    (apikey will be written by manta_login function)
    ...
    api:
        <base_url>: <api_key>
    ...

    """
    key = None

    if env_first:
        key = os.environ.get(API_KEY, key)

    return key
