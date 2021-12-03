import os
import re
import threading
from typing import BinaryIO

from manta_client.base import filenames

from ..libs import stream


class ThreadSafeWriter(object):
    """Wrapper for a file object that serializes writes."""

    def __init__(self, f: BinaryIO) -> None:
        self._f = f
        self._lock = threading.lock()

    def write(self, *args, **kargs) -> None:
        self._lock.acquire()
        try:
            self._f.write(*args, **kargs)
            self._f.flush()
        finally:
            self._lock.release()

    def close(self) -> None:
        self._lock.acquire()
        try:
            self._f.close()
        finally:
            self._lock.release()


class ConsoleWriter(ThreadSafeWriter):
    """
    For new line, there are differences btw Unix and Windows

    Unix: LF (\n)
    Windows:  CRLF (\r\n)
    """

    def __init__(self, f: BinaryIO) -> None:
        super(ConsoleWriter, self).__init__(f=f)
        self._buff = b""

    def write(self, data) -> None:  # type: ignore
        lines = re.split(b"\r\n|\n", data)
        ret = []  # type: ignore
        for line in lines:
            if line[:1] == b"\r":
                if ret:
                    ret.pop()
                elif self._buff:
                    self._buff = b""
            line = line.split(b"\r")[-1]
            if line:
                ret.append(line)
        if self._buff:
            ret.insert(0, self._buff)
        if ret:
            self._buff = ret.pop()
        super(ConsoleWriter, self).write(b"\n".join(ret) + b"\n")

    def close(self) -> None:
        if self._buff:
            super(ConsoleWriter, self).write(self._buff)
        super(ConsoleWriter, self).close()


class ConsoleSync(object):
    def __init__(self, experiment: str = None) -> None:
        self._experiment = experiment

        self._callback = None
        self._file = open(self.output_save_path, "wb")
        self._output_writer = ConsoleWriter(self._file)

    @property
    def output_save_path(self):
        dirpath = self._experiment._settings.files_dir
        filename = filenames.CONSOLE_FNAME
        return os.path.join(dirpath, filename)

    def set_callback(self, cb):
        # TODO: assert cb get arguments for stream_name(stderr, stdout) and data
        self._callback = cb

    def _sync_redirect(self):
        # TODO: implement here
        pass

    def _sync_wrap(self):
        out_sync = stream.StreamWrapper(
            src="stdout",
            cbs=[
                lambda data: self._callback("stdout", data),  # to server
                self._output_writer.write,  # to local
            ],
        )
        err_sync = stream.StreamWrapper(
            src="stderr",
            cbs=[
                lambda data: self._callback("stderr", data),
                self._output_writer.write,
            ],
        )
        return out_sync, err_sync

    def _sync_off(self):
        out_sync = None
        err_sync = None
        return out_sync, err_sync

    def sync(self, option):
        sync_init_func = getattr(self, f"_sync_{option}", None)
        if sync_init_func:
            out_sync, err_sync = sync_init_func()
        else:
            raise ValueError("console sync option is wrong(redirect, wrap, off")

        try:
            out_sync.install()
            err_sync.install()
            self._out_sync = out_sync
            self._err_sync = err_sync
        except Exception as e:
            print(e)
            print("Failed to console synchronize.", exc_info=e)
        return

    def _reset_handlers(self) -> None:
        if self._out_sync:
            self._out_sync.uninstall()
        if self._err_sync:
            self._err_sync.uninstall()
        return

    def stop(self):
        self._reset_handlers()

        if self._output_writer:
            self._output_writer.close()
            self._output_writer = None
