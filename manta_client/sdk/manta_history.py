import time


class History(object):
    def __init__(self, experiment):
        self._experiment = experiment
        self._step = 0
        self._data = dict()
        self._callback = None

        self._start_time = time.time()

    def __len__(self):
        return len(self._data)

    def __getitem__(self, __name: str):
        return self._data[__name]

    def _row_update(self, data):
        self._data.update(data)
        self.flush()

    def set_callback(self, cb):
        # TODO: check callback gets arguments for row
        self._callback = cb

    def flush(self):
        if len(self._data) > 0:
            self._data["_step"] = self._step
            self._data["_runtime"] = int(self._data.get("_runtime", time.time() - self._start_time))
            self._data["_timestamp"] = int(self._data.get("_timestamp", time.time()))
            if self._callback:
                self._callback(row=self._data)
            self._data = dict()


if __name__ == "__main__":
    import manta_client as mc

    exp = mc.init()
    exp.log({})
