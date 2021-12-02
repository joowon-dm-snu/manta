from typing import Optional

import manta_client.base.packet as pkt


def packet_to_json(packet):
    pass


class RouteManager:
    def __init__(self, api):
        self._api = api
        self.fs = FileStreamer(self._api)
        self.sm = SendManager(self.fs)

    def route_history(self, data):
        self.sm.send_history(data)


class SendManager:
    def __init__(self, fs):
        self.fs = fs

    def send_history(self, history):
        self.fs.push("manta_history", history)


class FileStreamer:
    def __init__(self, api):
        self.api = api
        self.buffer = {"manta_history": []}

        self.cnt = 0

    def body(self, file):
        if self.cnt >= 5:
            self.api.send_experiment_record(self.buffer[file])
            self.buffer[file] = []
            self.cnt = 0

    def push(self, file, data):
        self.buffer[file].append(data)
        self.cnt += 1

        self.body(file)


class Interface(object):
    def __init__(self, api):
        self._api = api
        self._router = RouteManager(self._api)  # TODO: remove direct router access. will be replaced to queue

    def _make_packet(self, packet):
        p = pkt.Packet.init_from(packet)
        return p

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
