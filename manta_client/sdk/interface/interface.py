from typing import Optional

import manta_client.base.packet as pkt

from ..manta_experiment import Experiment


class Interface(object):
    def __init__(self, experiment: Optional[Experiment] = None):
        self._buffer = []  # TODO: refactor here, this is temporal implementation
        self._experiment = experiment

    def set_experiment(self, experiment: Experiment):
        self._experiment = experiment
        self._api = experiment._api

    def _publish(self, packet: pkt.Packet) -> None:
        # TODO: for offline mode, need to set save = True
        # TODO: api calls will be called further back later
        return True

    def _publish_history(self, history: pkt.HistoryPacket) -> None:
        rec = self._make_packet(history=history)
        self._publish(rec)
        self._api.send_record()

    def publish_history(self, data: dict, step: int = None):
        run = run or self._run
        data = data_types.history_dict_to_json(run, data, step=step)
        history = pb.HistoryPacket()
        if publish_step:
            assert step is not None
            history.step.num = step
        data.pop("_step", None)
        for k, v in six.iteritems(data):
            item = history.item.add()
            item.key = k
            item.value_json = json_dumps_safer_history(v)  # type: ignore
        self._publish_history(history)
