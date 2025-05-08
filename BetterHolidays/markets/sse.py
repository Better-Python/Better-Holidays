from .market import Market
import datetime as dt
import zoneinfo as zi
from ..utils import classproperty
from .holidays import (
    ChineseNewYearsDay,
    NewYearsDay,
    QingMingFestival,
    ChineseLabourDay,
    DragonBoatFestival,
    ChineseNationalDay,
    AutumnFestival,
)


class SSE(Market):
    name = "Shanghai Stock Exchange"
    country = "China"
    include_country_holidays = True
    excluded_country_holidays = []

    tz = zi.ZoneInfo("Asia/Shanghai")

    standard_open_time = dt.time(hour=9, minute=15, tzinfo=tz)
    standard_close_time = dt.time(hour=15, minute=30, tzinfo=tz)

    abnormal_days = {}

    holidays = [
        NewYearsDay([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        ChineseNewYearsDay([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        QingMingFestival([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        ChineseLabourDay([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        DragonBoatFestival([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        AutumnFestival([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
        ChineseNationalDay([0, 1, 2, 3, 4], change={6: 1, 5: -1}),
    ]

    @classproperty
    def weekdays(cls):
        return [0, 1, 2, 3, 4]
