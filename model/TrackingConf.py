from typing import NamedTuple
from typing import TypedDict

from pydantic import BaseModel


class Daterange(NamedTuple):
    fromDate: str
    endDate: str


class TimerangeDict(TypedDict):
    key: str
    value: Daterange | None


class TrackingData(TypedDict):
    key: str
    value: TimerangeDict


class TrackingConf(BaseModel):
    dictionary: TrackingData = TrackingData({}, total=False)
