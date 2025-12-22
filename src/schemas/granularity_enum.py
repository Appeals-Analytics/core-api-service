from enum import Enum

class GranularityEnum(str, Enum):
  HOUR = "hour"
  DAY = "day"
  WEEK = "week"
  MONTH = "month"
