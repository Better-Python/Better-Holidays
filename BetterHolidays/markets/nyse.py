import BetterMD as md
from BetterMD import elements as elm
from .market import Market, classproperty
from .holidays import (
    NewYearsDay,
    MartinLutherKingJrDay,
    WashingtonsBirthday,
    LincolnsBirthday,
    GoodFriday,
    MemorialDay,
    JuneteenthNationalIndependenceDay,
    IndependenceDay,
    LaborDay,
    Thanksgiving,
    Christmas,
    CommonHoliday,
)
from ..days import Day, Holiday, TradingDay, PartialTradingDay, NonTradingDay
from ..const import MONTHS_MAP
from ..utils import iter_year
import datetime as dt
import zoneinfo as zi

# Standard open/close times = 9:30 - 4:00
# * Close at 1pm
# ** Closes at 1pm
# *** Closes at 1pm


class NYSE(Market):
    name = "NYSE"
    country = "US"
    include_country_holidays = True
    excluded_country_holidays = []

    tz = zi.ZoneInfo("America/New_York")

    standard_open_time = dt.time(hour=9, minute=30, tzinfo=tz)
    standard_close_time = dt.time(hour=16, tzinfo=tz)

    abnormal_days: "dict[dt.date, Day]" = {
        dt.date(1903, 2, 1): Holiday(
            date=dt.date(1903, 2, 1), name="Washington's Birthday"
        ),
        dt.date(1901, 2, 23): Holiday(
            date=dt.date(1901, 2, 23), name="Washington's Birthday"
        ),
        dt.date(1907, 2, 23): Holiday(
            date=dt.date(1907, 2, 23), name="Washington's Birthday"
        ),
        dt.date(1929, 2, 23): Holiday(
            date=dt.date(1929, 2, 23), name="Washington's Birthday"
        ),
        dt.date(1946, 2, 23): Holiday(
            date=dt.date(1911, 2, 23), name="Washington's Birthday"
        ),
        dt.date(2001, 9, 11): Holiday(date=dt.date(2001, 9, 11), name="9/11"),
        dt.date(2001, 9, 12): Holiday(date=dt.date(2001, 9, 12), name="9/11"),
        dt.date(2001, 9, 13): Holiday(date=dt.date(2001, 9, 13), name="9/11"),
        dt.date(2001, 9, 14): Holiday(date=dt.date(2001, 9, 14), name="9/11"),
        dt.date(2001, 9, 17): PartialTradingDay(
            name="9/11 moment of silence",
            date=dt.date(2001, 9, 17),
            open_time=dt.time(hour=9, minute=33),
            close_time=standard_close_time,
            late_open=True,
            late_open_reason="Moment of silence for 9/11",
        ),
        dt.date(2001, 10, 8): PartialTradingDay(
            name="Enduring Freedom",
            date=dt.date(2001, 10, 8),
            open_time=dt.time(hour=9, minute=31),
            close_time=standard_close_time,
            late_open=True,
            late_open_reason="Moment of silence for Enduring Freedom",
        ),
        dt.date(2002, 9, 11): PartialTradingDay(
            name="9/11 Anniversary",
            date=dt.date(2002, 9, 11),
            open_time=dt.time(hour=12),
            close_time=standard_close_time,
            late_open=True,
            late_open_reason="9/11 Anniversary",
        ),
        dt.date(2003, 2, 20): PartialTradingDay(
            name="Enduring Freedom",
            date=dt.date(2003, 2, 20),
            open_time=dt.time(hour=9, minute=32),
            close_time=standard_close_time,
            late_open=True,
            late_open_reason="Moment of silence for Enduring Freedom",
        ),
        dt.date(2004, 6, 7): PartialTradingDay(
            name="President Ronald Reagan's death",
            date=dt.date(2004, 6, 7),
            open_time=dt.time(hour=9, minute=32),
            close_time=standard_close_time,
            late_open=True,
            late_open_reason="Moment of silence for President Ronald Reagan's death",
        ),
        dt.date(2004, 6, 11): Holiday(
            date=dt.date(2004, 6, 11), name="Morning President Ronald Reagan's death"
        ),
        dt.date(2005, 6, 1): PartialTradingDay(
            name="President Ronald Reagan's death",
            date=dt.date(2005, 6, 1),
            open_time=standard_open_time,
            close_time=dt.time(hour=15, minute=36),
            early_close=True,
            early_close_reason="Moment of silence for President Ronald Reagan's death",
        ),
        dt.date(2006, 12, 27): PartialTradingDay(
            name="President Gerald Ford's death",
            date=dt.date(2006, 12, 27),
            open_time=dt.time(hour=9, minute=32),
            close_time=standard_close_time,
            late_open=True,
            late_open_reason="Moment of silence for President Gerald Ford's death",
        ),  #
        dt.date(2007, 1, 2): Holiday(
            date=dt.date(2007, 1, 2), name="Mourning of President Gerald Ford's death"
        ),
        dt.date(2012, 10, 29): Holiday(
            date=dt.date(2012, 10, 29), name="Hurricane Sandy"
        ),
        dt.date(2012, 10, 30): Holiday(
            date=dt.date(2012, 10, 30), name="Hurricane Sandy"
        ),
        dt.date(2018, 12, 5): Holiday(
            date=dt.date(2018, 12, 5), name="President George H.W. Bush's death"
        ),
        dt.date(2025, 1, 9): Holiday(
            date=dt.date(2025, 1, 9), name="President Jimmy Carter's death"
        ),
    }

    holidays: "list[CommonHoliday]" = [
        NewYearsDay(
            [0, 1, 2, 3, 4], change={6: 1, 5: -1}, start=dt.date(1952, 9, 29)
        ),  # Saturday -> Friday, Sunday -> Monday
        NewYearsDay(
            [0, 1, 2, 3, 4, 5], change={6: 1}, end=dt.date(1952, 9, 28)
        ),  # Saturday -> Friday, Sunday -> Monday
        MartinLutherKingJrDay(
            [0, 1, 2, 3, 4], change={6: 1, 5: -1}, start=dt.date(1998, 1, 1)
        ),
        WashingtonsBirthday([0, 1, 2, 3, 4], change={6: 1}, end=dt.date(1952, 9, 28)),
        WashingtonsBirthday(
            [0, 1, 2, 3, 4],
            change={6: 1, 5: -1},
            start=dt.date(1952, 9, 28),
            end=dt.date(1963, 12, 31),
        ),
        WashingtonsBirthday(
            [0, 1, 2, 3, 4],
            change={6: 1, 5: -1},
            start=dt.date(1964, 1, 1),
            end=dt.date(1970, 12, 31),
        ),
        LincolnsBirthday([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        GoodFriday([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        MemorialDay([0, 1, 2, 3, 4, 5], change={6: 1}, end=dt.date(1952, 9, 28)),
        MemorialDay(
            [0, 1, 2, 3, 4],
            change={6: 1, 5: -1},
            start=dt.date(1952, 9, 28),
            end=dt.date(1963, 12, 31),
        ),
        MemorialDay([0, 1, 2, 3, 4], change={6: 1, 5: -1}, start=dt.date(1964, 1, 1)),
        JuneteenthNationalIndependenceDay(
            [0, 1, 2, 3, 4], change={6: 1, 5: -1}, start=dt.date(2022, 1, 1)
        ),
        IndependenceDay([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        LaborDay([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        Thanksgiving([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        Christmas([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
    ]

    @classproperty
    def weekdays(cls):
        return [0, 1, 2, 3, 4]

    @classmethod
    def fetch_data(cls, year: "int"):
        if year < dt.date.today().year:
            return cls.fetch_past(year)
        else:
            return cls.fetch_future()

    @classmethod
    def fetch_past(cls, year: "int"):
        return super().fetch_data(year)

    @classmethod
    def get_day_type(cls, day: dt.date) -> "type[Day]":
        if day in cls.abnormal_days:
            return type(cls.abnormal_days[day])

        elif day.weekday() in cls.weekdays:
            return TradingDay

        else:
            return NonTradingDay

    @classmethod
    def fetch_future(cls):
        doc = md.HTML.from_url("https://www.nyse.com/markets/hours-calendars")
        table: "elm.Table" = doc.inner_html.get_elements_by_class_name("table-data")[0]

        table_dict = table.to_dict()
        holidays = table_dict.pop("Holiday")

        for year, dates in table_dict.items():

            def handle_date(date: "str", year: "int"):
                split_date = date.split(" ")

                return dt.date(
                    year,
                    int(MONTHS_MAP[split_date[1].upper()]),
                    int(split_date[2].replace("*", "")),
                )

            year = int(year)
            hol_dates = {handle_date(date, year): hol for date, hol in zip(dates, holidays)}

            for day in iter_year(int(year)):
                if day in hol_dates:
                    name = hol_dates[day]
                    if name.endswith("*"):
                        cls.cache.set(
                            PartialTradingDay(
                                date=day,
                                name=name.removesuffix("*"),
                                open_time=dt.time(hour=9, minute=30),
                                close_time=dt.time(hour=13),
                                early_close=True,
                                early_close_reason=name.removesuffix("*"),
                            ),
                        )
                    else:
                        cls.cache.set(Holiday(date=day, name=name))
                elif day.weekday() in cls.weekdays:
                    cls.cache.set(
                        TradingDay(
                            date=day,
                            open_time=cls.standard_open_time,
                            close_time=cls.standard_close_time,
                        ),
                    )
                else:
                    cls.cache.set(NonTradingDay(date=day))
