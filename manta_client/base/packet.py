from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

"""

Packet: Can be saved for offline or user wants
Request & Response: interaction with server 
"""


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
class _HistoryItem:
    key: str
    value: Union[str, int, float]


@dataclass
class HistoryPacket:
    item: List[_HistoryItem]
    step: int


@dataclass
class SummaryPacket:
    pass


@dataclass
class ConsolePacket:
    stream: str  # stderr or stdout
    timestamp: int
    lines: str


@dataclass
class _StatsItem:
    key: str
    value: Dict


@dataclass
class StatsPacket:
    item: List[_StatsItem]
    timestamp: int
    step: int


@dataclass
class ArtifactPacket:
    experiment_id: str
    experiment_name: str
    project: str
    entity: str
    checksum: str
    description: str
    contents: List["ArtifactManifest"]


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
class AlarmPacket:
    title: str
    text: str
    level: str


@dataclass
class ExperimentPacket:
    experiment_id: str
    entity: str
    project: str


@dataclass
class SettingsPacket:
    pass


@dataclass
class ConfigPacket:
    pass


@dataclass
class MetaPacket:
    group: str
    job: str


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
