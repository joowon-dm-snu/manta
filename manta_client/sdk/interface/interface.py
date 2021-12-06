from typing import Any, Dict, Optional

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
        history = packet.history.item
        self.fs.push("histories", history)

    def send_stats(self, packet: pkt.Packet):
        # self._flatten(row)
        # row["_wandb"] = True
        # row["_timestamp"] = now
        # row["_runtime"] = int(now - self._run.start_time.ToSeconds())
        stats = packet.stats
        self.fs.push("systems", stats)

    def send_console(self, packet: pkt.Packet):
        console = packet.console
        self.fs.push("logs", console)


class ApiStreamer:
    def __init__(self, api):
        self.api = api
        self._buffer = None
        self._cnt = 0
        self._reset_buffer()

    def _reset_buffer(self):
        self._buffer = dict(
            histories=[],
            systems=[],
            logs=[],
        )
        self._cnt = 0

    def body(self):
        if self._cnt >= 5:
            self.api.send_experiment_record(**self._buffer)
            self._reset_buffer()

    def push(self, file, data):
        self._buffer[file].append(data)
        self._cnt += 1

        self.body()


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
        history = pkt.HistoryPacket(data)
        self._publish_history(history)

    def _publish_stats(self, stats: pkt.StatsPacket) -> None:
        packet = self._wrap_packet(stats)
        self._handler.handle_stats(packet)
        # self._publish(packet)

    def publish_stats(self, data: dict):
        # TODO: sync step with history
        self._publish_stats({"item": data})

    def _publish_console(self, console: pkt.ConsolePacket) -> None:
        packet = self._wrap_packet(console)
        self._handler.handle_console(packet)
        # self._publish(packet)

    def publish_console(self, data: dict):
        self._publish_console({"item": data})
