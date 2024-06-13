from datetime import datetime
from enum import Enum

from pydantic import BaseModel 


class Group(str, Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class PeriodData(BaseModel):
    dt_from: datetime
    dt_upto: datetime
    group_type: Group
