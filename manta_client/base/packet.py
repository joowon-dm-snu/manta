from dataclasses import dataclass
from typing import Any, Dict, Union

"""
Packet & Result: Can be saved for offline or user wants
Request & Response: 
"""


@dataclass
class Packet:
    key: str
    value: Any

    @classmethod
    def init_from(cls, obj):
        k = obj.__class__.__name__.lower().replace("packet", "")
        packet = cls(key=k, value=obj)
        packet.__setattr__(k, obj)
        return packet


@dataclass
class HistoryItem:
    key: str
    value: Union[str, int, float]


@dataclass
class HistoryPacket:
    item: HistoryItem
    step: int


@dataclass
class StatsItem:
    key: str
    value: Dict


@dataclass
class StatsPacket:
    item: StatsItem
    timestamp: int
    step: int


@dataclass
class Result:
    pass


@dataclass
class Request:
    pass


@dataclass
class Response:
    pass
