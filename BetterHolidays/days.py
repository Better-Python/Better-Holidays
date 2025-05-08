import peewee as pw
from . import utils


class Day(pw.Model):
    """Base class representing a calendar day."""

    class Meta:
        database = utils.get_db()

    date = pw.DateField(primary_key=True)
    market = pw.CharField(null=True)

class Holiday(Day):
    """Represents a full holiday (market closed)."""

    name = pw.CharField()


class TradingDay(Day):
    """Represents a full trading day with standard open/close times."""

    open_time = pw.TimeField()
    close_time = pw.TimeField()


class NonTradingDay(Day):
    """Represents a non-trading day (e.g. weekends)."""

    pass


class PartialTradingDay(TradingDay, Holiday):
    """Represents a partial trading day (early close or late open)."""

    early_close = pw.BooleanField(default=False)
    late_open = pw.BooleanField(default=False)
    early_close_reason = pw.CharField(default="")
    late_open_reason = pw.CharField(default="")
