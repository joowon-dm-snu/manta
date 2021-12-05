from typing import Any, Dict, Optional

import manta_client.base.packet as pkt
from manta_client import Settings

from ..manta_experiment import Experiment

"""
Interface -> Handler -> Store(Future Implement) -> Sender -> ApiStreamer

Interface: create packets, pass it to handler
Handler: handle packets, execute complex logics 
Sender: send packets or request to server 
"""


def packet_to_json(packet):
    pass


# TODO: split classes to internal files


class RouteManager:
    def __init__(self, api):
        self._api = api
        self.fs = ApiStreamer(self._api)
        self.sm = SendManager(self.fs)

    def route_history(self, data):
        self.sm.send_history(data)

    def route_history(self, data):
        self.sm.send_stats(data)

    def route_console(self, data):
        self.sm.send_console(data)


class SendManager:
    def __init__(self, fs):
        self.fs = fs

    def send_history(self, history):
        self.fs.push("histories", history)

    def send_stats(self, stats):
        self.fs.push("systems", stats)

    def send_console(self, console):
        self.fs.push("logs", console)


class ApiStreamer:
    def __init__(self, api):
        self.api = api
        self.buffer = dict()

        self._cnt = 0

    def body(self):
        if self._cnt >= 5:
            self.api.send_experiment_record(**self.buffer)
            self.buffer = dict()
            self._cnt = 0

    def push(self, file, data):
        self.buffer[file].append(data)
        self._cnt += 1

        self.body()


class Interface(object):
    def __init__(self, api):
        self._api = api
        self._router = RouteManager(self._api)  # TODO: remove direct router access. will be replaced to queue

    def _make_packet(self, packet):
        p = pkt.Packet.init_from(packet)
        return p

    def _make_artifact(self, artifact: Any) -> pkt.ArtifactPacket:
        pass

    def _make_artifact_manifest(self, manifest) -> pkt.ArtifactManifest:
        pass

    def _make_summary(self, summary: Any) -> pkt.SummaryPacket:
        pass

    def _make_experiment(self, exp: Experiment) -> pkt.ExperimentPacket:
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
        packet = self._make_packet(history)
        self._router.route_history(history)
        # self._publish(packet)

    def publish_history(self, data: dict, step: int = None):
        self._publish_history({"step": step, "item": data})

    def _publish_stats(self, stats: pkt.StatsPacket) -> None:
        packet = self._make_packet(stats)
        self._router.route_stats(stats)
        # self._publish(packet)

    def publish_stats(self, data: dict):
        # TODO: sync step with history
        self._publish_stats({"item": data})

    def _publish_console(self, console: pkt.ConsolePacket) -> None:
        packet = self._make_packet(console)
        self._router.route_console(console)
        # self._publish(packet)

    def publish_console(self, data: dict):
        # TODO: sync step with history
        self._publish_console({"item": data})
