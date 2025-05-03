import dataclasses as dc
import datetime as dt

@dc.dataclass(frozen=True)
class Day:
    """Base class representing a calendar day."""
    date: dt.date

@dc.dataclass(frozen=True)
class Holiday(Day):
    """Represents a full holiday (market closed)."""
    name: str

@dc.dataclass(frozen=True)
class TradingDay(Day):
    """Represents a full trading day with standard open/close times."""
    open_time: dt.time
    close_time: dt.time

@dc.dataclass(frozen=True)
class NonTradingDay(Day):
    """Represents a non-trading day (e.g. weekends)."""
    pass

@dc.dataclass(frozen=True)
class PartialTradingDay(TradingDay, Holiday):
    """Represents a partial trading day (early close or late open)."""
    name: str
    early_close: bool = False
    late_open: bool = False
    early_close_reason: str = ""
    late_open_reason: str = ""
