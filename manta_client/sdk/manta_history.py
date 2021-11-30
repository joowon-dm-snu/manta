class History(object):
    def __init__(self, experiment):
        self._experiment = experiment
        self._step = 0
        self._data = dict()
        self._callback = self._default_callback

    def __len__(self):
        return len(self._data)

    def __getitem__(self, __name: str):
        return self._data[__name]

    def _row_update(self, data):
        self._data.update(data)

    def _default_callback(self):
        pass

    def set_callback(self):
        pass

    def flush(self):
        # TODO: add api and make here compatible
        self._experiment._backend._api.send_experiment_record()
