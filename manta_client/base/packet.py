import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

"""

Packet: Can be saved for offline or user wants
Request & Response: interaction with server 
"""


@dataclass
class _PacketDefault(object):
    _timestamp: int = None

    def as_dict(self):
        res = dict()
        return self.__dict__

    def __post_init__(self):
        self._timestamp = int(time.time() * 1000)


@dataclass
class Packet:
    key: str
    value: Any
    req_result: int = 0  # 0 for false, 1 for true
    result: Optional["Response"] = None

    # Like heartbeats
    history: Optional["HistoryPacket"] = None
    summary: Optional["SummaryPacket"] = None
    console: Optional["ConsolePacket"] = None
    stats: Optional["StatsPacket"] = None
    # Less frequent
    artifact: Optional["ArtifactPacket"] = None
    alarm: Optional["AlarmPacket"] = None
    experiment: Optional["ExperimentPacket"] = None
    settings: Optional["SettingsPacket"] = None
    config: Optional["ConfigPacket"] = None
    meta: Optional["MetaPacket"] = None

    @classmethod
    def init_from(cls, obj):
        k = obj.__class__.__name__.lower().replace("packet", "")
        packet = cls(key=k, value=obj)
        packet.__setattr__(k, obj)
        return packet


@dataclass
class HistoryPacket(_PacketDefault):
    item: Dict[str, Union[str, int, float]] = None


@dataclass
class SummaryPacket(_PacketDefault):
    pass


@dataclass
class ConsolePacket(_PacketDefault):
    lines: str = None
    _stream: str = None  # stderr or stdout


@dataclass
class _StatsItem:
    key: str
    value: Dict


@dataclass
class StatsPacket(_PacketDefault):
    item: List[_StatsItem] = None
    _step: int = None


@dataclass
class ArtifactPacket(_PacketDefault):
    experiment_id: str = None
    experiment_name: str = None
    project: str = None
    entity: str = None
    checksum: str = None
    description: str = None
    contents: List["ArtifactManifest"] = None


@dataclass
class ArtifactManifest:
    version: int
    zipped: bool
    storage: str
    detail: "ArtifactManifestDetail"


@dataclass
class ArtifactManifestDetail:
    path: str
    checksum: str
    size: int
    local_path: str


@dataclass
class AlarmPacket(_PacketDefault):
    title: str = None
    text: str = None
    level: str = None


@dataclass
class ExperimentPacket(_PacketDefault):
    experiment_id: str = None
    entity: str = None
    project: str = None


@dataclass
class SettingsPacket(_PacketDefault):
    pass


@dataclass
class ConfigPacket(_PacketDefault):
    pass


@dataclass
class MetaPacket(_PacketDefault):
    group: str = None
    job: str = None


@dataclass
class Request:
    pass


@dataclass
class Response:
    pass


@dataclass
class LoginRequest:
    pass


@dataclass
class LoginResponse:
    pass


@dataclass
class ExperimentStartRequest:
    pass


@dataclass
class ExperimentStartResponse:
    pass


@dataclass
class ArtifactRequest:
    pass


@dataclass
class ArtifactResponse:
    pass
