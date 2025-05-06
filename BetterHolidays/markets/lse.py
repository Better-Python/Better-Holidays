from .market import Market
import datetime as dt
from ..days import Day, Holiday, TradingDay, PartialTradingDay, NonTradingDay
from ..const import MONTHS_MAP
import BetterMD as md
import re

class LSE(Market):
    name = "London Stock Exchange"
    country = "UK"
    include_country_holidays = True
    excluded_country_holidays = []

    standard_open_time = dt.time(hour=9, minute=30)
    standard_close_time = dt.time(hour=16)

    abnormal_days = {}

    REGEX = re.compile(r"(\d+) ([a-zA-Z]+) (\d+)")

    @classproperty
    def weekdays(cls):
        return [0,1,2,3,4]
    
    @classmethod
    def fetch_data(cls, year: 'int'):
        try:
            table:'md.elements.Table' = md.HTML.from_url(f"https://www.calendar-365.co.uk/holidays/{year}.html").inner_html.get_elements_by_class_name("table")[0]
            holidays = {}

            for tr in table.body[0]:
                day, month, _ = cls.REGEX.match(tr.children[0].text).groups()
                date = dt.date(year, MONTHS_MAP[month.upper()], int(day))
                holidays[date] = Holiday(date, name=tr.children[1].text)

        except Exception as e:
            raise ValueError(f"Error fetching LSE data for {year}: {e}")

        return holidays