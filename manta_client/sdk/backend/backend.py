from manta_client.sdk.interface.interface import Interface


class Backend(object):
    def __init__(self, api=None) -> None:
        self._api = api

        self.interface = None

    def _setup_interface(self):
        self.interface = Interface(self._api)

    def init_internal_process(self):
        self._setup_interface()

    def cleanup(self):
        self.interface.finish()
