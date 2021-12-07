import manta_client.base as manta_base

Settings = manta_base.Settings
Config = manta_base.Config

from manta_client import env, sdk, utils

__version__ = "0.1.0.dev1"

init = sdk.init
setup = sdk.setup
login = sdk.login


# global vars
experiment = None
config = None
meta = None

# global functions
log = None
save = None
alarm = None
use_artifact = None
log_artifact = None

__all__ = [
    "__version__",
    "init",
    "setup",
    "login",
    "Settings",
    "Config",
    "experiment",
    "config",
    "meta",
    "log",
    "save",
    "alarm",
    "use_artifact",
    "log_artifact",
]
