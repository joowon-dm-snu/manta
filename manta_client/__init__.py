from manta_client import sdk

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
    "experiment",
    "config",
    "meta",
    "log",
    "save",
    "alarm",
    "use_artifact",
    "log_artifact",
]
