import collections
import itertools
import queue
import threading
import time
from typing import Any, Dict, Optional

import manta_client as mc
import manta_client.base.packet as pkt
from manta_client import Settings

# from ..manta_experiment import Experiment

"""
Interface -> Handler -> Store(Future Implement) -> Sender -> ApiStreamer

Interface: create packets, pass it to handler
Handler: handle packets, execute complex logics 
Sender: send packets or request to server 
"""


def packet_to_json(packet):
    pass


# TODO: split classes to internal files


class HandleManager:
    def __init__(self, api):
        self._api = api
        self.fs = ApiStreamer(self._api)
        self.sm = SendManager(self.fs)

        self.fs.start()

    def handle_history(self, packet: pkt.Packet):
        self.sm.send_history(packet)

    def handle_stats(self, packet: pkt.Packet):
        self.sm.send_stats(packet)

    def handle_console(self, packet: pkt.Packet):
        self.sm.send_console(packet)


class SendManager:
    def __init__(self, fs):
        self.fs = fs

    def send_history(self, packet: pkt.Packet):
        history = packet.history.as_dict()
        self.fs.push("histories", history)

    def send_stats(self, packet: pkt.Packet):
        # self._flatten(row)
        # row["_wandb"] = True
        # row["_timestamp"] = now
        # row["_runtime"] = int(now - self._run.start_time.ToSeconds())
        stats = packet.stats.as_dict()
        self.fs.push("systems", stats)

    def send_console(self, packet: pkt.Packet):
        console = packet.console.as_dict()
        self.fs.push("logs", console)


Item = collections.namedtuple("Item", ("filename", "data"))
FinishItem = collections.namedtuple("FinishItem", ("exitcode"))


class ApiStreamer:
    # WARNING: DO NOT CHANGE VALUES BELOW, API WILL REJECT YOUR REQUEST.
    HEARTBEAT_SECONDS = 30
    MAX_ITEMS_PER_PUSH = 10000

    def __init__(self, api, start_time=None):
        self.api = api
        self._start_time = start_time or time.time()

        self._queue = queue.Queue()
        self._cnt = 0
        self._thread = None

    def debounce_seconds(self):
        run_time = time.time() - self._start_time
        if run_time < 60:
            return self.HEARTBEAT_SECONDS / 15
        elif run_time < 300:
            return self.HEARTBEAT_SECONDS / 3
        else:
            return self.HEARTBEAT_SECONDS

    def _read_queue(self):
        wait_seconds = self.debounce_seconds()
        return mc.util.read_many_from_queue(self._queue, self.MAX_ITEMS_PER_PUSH, wait_seconds)

    def _process_fileitem(self, items):
        res = []
        for item in items:
            res.append(item.data)

        return res

    def _aggregate_send(self, buffer):
        files = {}
        # Groupby needs group keys to be sorted
        buffer.sort(key=lambda c: c.filename)
        for filename, file_items in itertools.groupby(buffer, lambda c: c.filename):
            files[filename] = self._process_fileitem(file_items)
        self.api.send_experiment_record(**files)

    def _heartbeat_send(self):
        self.api.send_heartbeat()

    def _thread_body(self):
        buffer = []
        latest_post_time = time.time()
        latest_heartbeat_time = time.time()
        finished = None
        while finished is None:
            items = self._read_queue()
            for item in items:
                if isinstance(item, FinishItem):
                    finished = item
                else:
                    buffer.append(item)

            cur_time = time.time()
            if buffer and cur_time - latest_post_time > self.debounce_seconds():
                latest_post_time = cur_time
                latest_heartbeat_time = cur_time
                self._aggregate_send(buffer)
                buffer = []

            # if stats are disabled, theres something we need to send heartbeat to server for tracking experiment status
            if cur_time - latest_heartbeat_time > self.HEARTBEAT_SECONDS:
                latest_heartbeat_time = cur_time
                self._heartbeat_send()

        # TODO: send api stream finished to server
        pass

    def start(self):
        self._thread = threading.Thread(target=self._thread_body)
        self._thread.name = "ApiStreamThread"
        self._thread.daemon = True
        self._thread.start()

    def push(self, file, data):
        self._queue.put(Item(file, data))

    def finish(self, exitcode):
        """Cleans up.
        finish thread by add finish item in queue

        Arguments:
            exitcode: The exitcode of the watched process.
        """
        self._queue.put(FinishItem(exitcode))
        # TODO: cleaning
        self._thread.join()
        # TODO: show exception info


class Interface(object):
    def __init__(self, api):
        self._api = api
        self._handler = HandleManager(self._api)  # TODO: remove direct handler access. will be replaced to queue

    def _wrap_packet(self, packet):
        p = pkt.Packet.init_from(packet)
        return p

    def _make_artifact(self, artifact: Any) -> pkt.ArtifactPacket:
        pass

    def _make_artifact_manifest(self, manifest) -> pkt.ArtifactManifest:
        pass

    def _make_summary(self, summary: Any) -> pkt.SummaryPacket:
        pass

    def _make_experiment(self, exp: "Experiment") -> pkt.ExperimentPacket:
        pass

    def _make_settings(self, settings: Settings) -> pkt.SettingsPacket:
        pass

    def _make_config(self, config: Dict) -> pkt.ConfigPacket:
        pass

    def _make_meta(self, meta: Dict) -> pkt.MetaPacket:
        pass

    def _publish(self, packet: pkt.Packet) -> None:
        # TODO: for offline mode, need to set save = True
        # TODO: api calls will be called further back later
        return True

    def _publish_history(self, history: pkt.HistoryPacket) -> None:
        packet = self._wrap_packet(history)
        self._handler.handle_history(packet)
        # self._publish(packet)

    def publish_history(self, data: dict):
        history = pkt.HistoryPacket(item=data)
        self._publish_history(history)

    def _publish_stats(self, stats: pkt.StatsPacket) -> None:
        packet = self._wrap_packet(stats)
        self._handler.handle_stats(packet)
        # self._publish(packet)

    def publish_stats(self, data: dict):
        # TODO: sync step with history
        stats = pkt.StatsPacket(item=data)
        self._publish_stats(stats)

    def _publish_console(self, console: pkt.ConsolePacket) -> None:
        packet = self._wrap_packet(console)
        self._handler.handle_console(packet)
        # self._publish(packet)

    def publish_console(self, _stream, lines):
        console = pkt.ConsolePacket(_stream=_stream, lines=lines)
        self._publish_console(console)
