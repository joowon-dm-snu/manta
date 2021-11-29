__version__ = "0.1.0"

import manta_client as mc

from .base import Config, Settings
from .sdk import init, login, setup

# TODO: these initial globals should be init when mc.init is called.
mc.config = Config()
mc.setting = Settings()
