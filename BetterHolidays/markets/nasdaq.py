import datetime as dt
from ..days import Day, Holiday, TradingDay, PartialTradingDay, NonTradingDay
from ..const import MONTHS_MAP
from ..utils import iter_year, classproperty
from .market import Market
from .holidays import (
    NewYearsDay,
    MartinLutherKingJrDay,
    WashingtonsBirthday,
    GoodFriday,
    MemorialDay,
    JuneteenthNationalIndependenceDay,
    IndependenceDay,
    LaborDay,
    Thanksgiving,
    Christmas,
    ConsistentAbnormalDay,
)
import BetterMD as md
import zoneinfo as zi


class NASDAQ(Market):
    name = "NASDAQ"
    country = "US"
    include_country_holidays = True
    excluded_country_holidays = []

    tz = zi.ZoneInfo("America/New_York")

    standard_open_time = dt.time(hour=9, minute=30, tzinfo=tz)
    standard_close_time = dt.time(hour=16, tzinfo=tz)

    abnormal_days: "dict[dt.date, Day]" = {}

    holidays = [
        NewYearsDay([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        MartinLutherKingJrDay([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        WashingtonsBirthday([0, 1, 2, 3, 4], change={6: 1}),
        GoodFriday([0, 1, 2, 3, 4], change={6: 1}),
        MemorialDay([0, 1, 2, 3, 4, 5], change={6: 1}),
        JuneteenthNationalIndependenceDay([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        ConsistentAbnormalDay(
            "Independence Day",
            [0, 1, 2, 3, 4],
            change={6: 1, 5: -1},
            month=7,
            day=3,
            type=PartialTradingDay,
            open_time=dt.time(hour=9, minute=30),
            close_time=dt.time(hour=13),
            early_close=True,
            late_open=True,
            holiday_reason="Independence Day",
        ),
        IndependenceDay([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        LaborDay([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        Thanksgiving([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        ConsistentAbnormalDay(
            "Thanksgiving",
            [0, 1, 2, 3, 4],
            change={6: 1, 5: -1},
            month=11,
            day=27,
            type=PartialTradingDay,
            open_time=dt.time(hour=9, minute=30),
            close_time=dt.time(hour=13),
            early_close=True,
            late_open=True,
            holiday_reason="Thanksgiving",
        ),
        ConsistentAbnormalDay(
            "Christmas",
            [0, 1, 2, 3, 4],
            change={6: 1, 5: -1},
            month=12,
            day=24,
            type=PartialTradingDay,
            open_time=dt.time(hour=9, minute=30),
            close_time=dt.time(hour=13),
            early_close=True,
            late_open=True,
            holiday_reason="Christmas",
        ),
        Christmas([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
    ]

    @classproperty
    def weekdays(cls):
        return [0, 1, 2, 3, 4]

    @classmethod
    def fetch_data(cls, year: "int"):
        if year < dt.date.today().year:
            return cls.fetch_past(year)
        elif year == dt.date.today().year:
            return cls.fetch_future()

    @classmethod
    def fetch_past(cls, year: "int"):
        return super().fetch_data(year)

    @classmethod
    def fetch_future(cls):
        page = md.HTML.from_url(
            f"https://www.nasdaq.com/market-activity/stock-market-holiday-schedule"
        )
        table: "md.elements.Table" = page.inner_html.get_elements_by_class_name(
            "nsdq_table"
        )[0]
        holidays = {}
        for tr in table.body[0]:
            name, day, status = (
                tr.children[0].text,
                tr.children[1].text,
                tr.children[2].text,
            )

            month, date = day.split(" ")
            date = dt.date(dt.date.today().year, MONTHS_MAP[month.upper()], int(date))

            if status == "Closed":
                holidays[date] = Holiday(date=date, name=name)

            elif name == "Early Close":
                time, period = status.split(" ")
                hour, minute = time.split(":")
                time = dt.datetime.combine(
                    date, dt.time(hour=int(hour), minute=int(minute))
                )
                if period == "p.m.":
                    time = time + dt.timedelta(hours=12)

                time = time.time()

                holidays[date] = PartialTradingDay(
                    date=date,
                    name=name,
                    open_time=cls.standard_open_time,
                    close_time=time,
                    early_close=True,
                    early_close_reason=name,
                )
            else:
                holidays[date] = Holiday(date=date, name=name)

        for day in iter_year(dt.date.today().year):
            if day in holidays:
                cls.cache.set(holidays[day])
            elif day.weekday() in cls.weekdays:
                cls.cache.set(
                    TradingDay(
                        date=day,
                        open_time=cls.standard_open_time,
                        close_time=cls.standard_close_time,
                    )
                )
            else:
                cls.cache.set(NonTradingDay(date=day))
