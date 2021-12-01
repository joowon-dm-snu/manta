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

    def _default_callback(self, row, step):
        if self._backend and self._backend.interface:
            self._backend.interface.publish_history(
                row, step
            )


    def set_callback(self, cb):
        # TODO: check callback gets arguments for row and step
        self._callback = cb

    def flush(self):
        if len(self._data) > 0:
            self._data["_step"] = self._step
            self._data["_runtime"] = int(self._data.get("_runtime", time.time() - self.start_time))
            self._data["_timestamp"] = int(self._data.get("_timestamp", time.time()))
            if self._callback:
                self._callback(row=self._data, step=self._step)
            self._data = dict()
        # TODO: add api and make here compatible
        self._experiment._backend._api.send_experiment_record()


if __name__ == "__main__":
    import manta_client as mc

    exp = mc.init()
    exp.log({})
