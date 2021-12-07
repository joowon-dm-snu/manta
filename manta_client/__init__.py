from manta_client import sdk

__version__ = "0.1.0.dev1"

init = sdk.init
setup = sdk.setup
login = sdk.login


# global vars
config = None
meta = None
experiment = None

# global functions
log = None


__all__ = ["__version__", "init", "setup", "login", "config", "meta", "experiment", "log"]
