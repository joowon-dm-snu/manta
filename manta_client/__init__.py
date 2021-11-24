import manta_client as mc
from manta_client.base.config import Config
from manta_client.base.setting import Settings


# TODO: these initial globals should be init when mc.init is called.
mc.config = Config()
mc.setting = Settings()
