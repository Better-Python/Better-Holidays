import datetime as dt
from ..days import Day, Holiday, TradingDay, PartialTradingDay, NonTradingDay
from ..const import MONTHS_MAP
from ..utils import iter_year
from .market import Market


class NASDAQ(Market):
    name = "NASDAQ"
    country = "US"
    include_country_holidays = True
    excluded_country_holidays = []

    standard_open_time = dt.time(hour=9, minute=30)
    standard_close_time = dt.time(hour=16)

    abnormal_days: 'dict[dt.date, Day]' = {}

    @classmethod
    def fetch_data(cls, year: int):
        return 