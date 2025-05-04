import datetime as dt
import typing as t
from abc import ABC, abstractmethod
from ..days import Day, Holiday, TradingDay, PartialTradingDay
from ..const import DAYS_TYPE
from ..utils import iterate_date, abstract_const, classproperty
from .cache import Cache

class Market(ABC):
    cache: 'Cache'

    def __init_subclass__(cls) -> None:
        cls.cache = Cache()

    name = abstract_const()
    country = abstract_const()
    include_country_holidays = abstract_const()
    excluded_country_holidays = abstract_const()
    _weekends = None

    @classmethod
    def validate_options(cls):
        assert isinstance(cls.name, str), "Market name must be a string"
        assert isinstance(cls.country, str), "Country must be a string"
        assert isinstance(cls.include_country_holidays, bool), "Include country holidays must be a boolean"
        assert isinstance(cls.excluded_country_holidays, list), "Excluded country holidays must be a list"

    @classproperty
    @abstractmethod
    def weekdays(cls) -> DAYS_TYPE:
        """
        Return list of integers representing weekdays when market can be open.
        Monday=0 ... Sunday=6
        """
        ...

    @classproperty
    def weekends(cls) -> DAYS_TYPE:
        """
        Return list of integers representing standard non-trading weekend days.
        """
        if cls._weekends is None:
            cls._weekends = [i for i in range(7) if i not in cls.weekdays]

        return cls._weekends

    @classmethod
    @abstractmethod
    def fetch_data(cls, year: 'int'):
        """
        Fetch data between start and end dates.
        Must be implemented by subclasses.
        """
        ...

    @classmethod
    def get_holidays(cls, start: 'dt.date', end: 'dt.date') -> list[Holiday]:
        """Return list of holidays between start and end dates."""
        return list(filter(lambda d: isinstance(d, Holiday), [cls.day(day) for day in iterate_date(start, end)]))

    @classmethod
    def get_partial_days(cls, start: 'dt.date', end: 'dt.date') -> 'list[PartialTradingDay]':
        return list(filter(lambda d: isinstance(d, PartialTradingDay), [cls.day(day) for day in iterate_date(start, end)]))

    @classmethod
    def get_trading_days(cls, start: 'dt.date', end: 'dt.date') -> list[TradingDay]:
        """Return list of trading days between start and end dates."""
        return list(filter(lambda d: isinstance(d, TradingDay), [cls.day(day) for day in iterate_date(start, end)]))

    @classmethod
    def is_weekday(cls, date: 'dt.date') -> bool:
        return date.weekday() in cls.weekdays

    @classmethod
    def is_weekend(cls, date: 'dt.date') -> bool:
        return date.weekday() in cls.weekends

    @classmethod
    def is_holiday(cls, date: 'dt.date') -> bool:
        day = cls.day(date)
        if not isinstance(day, Holiday):
            return False
        return True

    @classmethod
    def is_partial_day(cls, date: 'dt.date') -> 'bool':
        day = cls.day(date)
        if not isinstance(day, PartialTradingDay):
            return False
        return True

    @classmethod
    def is_trading_day(cls, date: 'dt.date') -> 'bool':
        day = cls.day(date)
        if not isinstance(day, TradingDay):
            return False
        return True

    @classmethod
    def get_trading_day(cls, date: 'dt.date') -> 't.Optional[TradingDay]':
        day = cls.day(date)
        if not isinstance(day, TradingDay):
            return None
        return day

    @classmethod
    def day(cls, date: 'dt.date') -> 'Day':
        return cls.cache.get_or_set(date, cls.fetch_data)