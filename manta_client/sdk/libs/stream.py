import queue
import sys
import threading
import time

_global_streams = {"stdout": None, "stderr": None}

DEBOUNCE_SECONDS = 3


class StreamBase(object):
    def __init__(self, src, callbacks=None):
        assert hasattr(sys, src)
        self.src = src
        self.callbacks = callbacks or []

    @property
    def src_stream(self):
        return getattr(sys, "__%s__" % self.src)

    @property
    def src_fd(self):
        return self.src_stream.fileno()

    @property
    def original_stream(self):
        return getattr(sys, self.src)

    def install(self):
        curr_redirect = _global_streams.get(self.src)
        if curr_redirect and curr_redirect != self:
            curr_redirect.uninstall()
        _global_streams[self.src] = self

    def uninstall(self):
        if _global_streams[self.src] != self:
            return
        _global_streams[self.src] = None


class StreamWrapper(StreamBase):
    """
    Patches the write method of current sys.stdout/sys.stderr
    """

    def __init__(self, src, callbacks=()):
        super(StreamWrapper, self).__init__(src=src, callbacks=callbacks)
        self._installed = False
        self._queue = None
        self._stopped = None
        self._old_write = None

    def _read_queue(self):
        data = []
        # TODO: Need lock?
        while not self._queue.empty():
            data.append(self._queue.get())
        return data

    def _flush(self, _data=None):
        data = self._read_queue()
        if _data:
            data.extend(_data)

        for cb in self.callbacks:
            try:
                cb(data)
            except Exception:
                # TODO: reraise?
                pass

    def _thread_body(self):
        while not (self._stopped.is_set() and self._queue.empty()):
            self._flush()
            time.sleep(DEBOUNCE_SECONDS)

    def install(self):
        super(StreamWrapper, self).install()
        if self._installed:
            return
        stream = self.original_stream
        self._old_write = stream.write

        def write(data):
            self._old_write(data)
            self._queue.put(data)

        stream.write = write

        self._queue = queue.Queue()
        self._stopped = threading.Event()

        # # TODO: check experiment initiated? settings online?
        self._thread = threading.Thread(target=self._thread_body)
        self._thread.daemon = True
        self._thread.start()
        self._installed = True

    def uninstall(self):
        if not self._installed:
            return
        self.original_stream.write = self._old_write

        self._stopped.set()
        # if self._thread.is_alive():
        #     self._thread.join()
        self.flush()
        self._installed = False
        super(StreamWrapper, self).uninstall()


if __name__ == "__main__":
    f = open("test_log.txt", "wb")
    try:
        write = lambda data: f.write("".join(data).encode("utf-8"))

        s = StreamWrapper("stdout", [write])
        s.install()

        for i in range(100):
            print(i)

            if i % 10 == 0:
                s._flush()

    finally:
        f.close()
