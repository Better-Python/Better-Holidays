import datetime as dt
import typing as t
from abc import ABC, abstractmethod
from ..days import Day, Holiday, TradingDay, PartialTradingDay
from ..const import MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY, DAYS_TYPE

class Cache:
    def __init__(self):
        self.cache: dict[dt.date, Day] = {}

    def get(self, key: dt.date) -> Day|None:
        return self.cache.get(key)

    def set(self, key: dt.date, value: Day):
        self.cache[key] = value

    def get_or_set(self, key: dt.date, func: t.Callable[[int], None]) -> Day:
        if key in self.cache:
            return self.get(key)
        func(key.year)
        if key in self.cache:
            return self.get(key)
        raise ValueError("Cache miss")

    def clear(self):
        self.cache.clear()

    def pop(self, key: dt.date) -> t.Any:
        return self.cache.pop(key)

    def __contains__(self, key: dt.date) -> bool:
        return key in self.cache

def not_set(type_: str, attr: str):
    raise AttributeError(f"Can't {type_} attribute {attr}")

T = t.TypeVar('T')
T1 = t.TypeVar('T1')

ClassMethod = t.Callable[[T], T1]

class classproperty(t.Generic[T, T1]):
    def __init__(self, getter: ClassMethod[T, T1]):
        self.getter = getter
        self.setter = lambda val: not_set("set", self.getter.__name__)
        self.deleter = lambda: not_set("delete", self.getter.__name__)

    def set(self, method: ClassMethod[T, None]):
        self.setter = method
        return self

    def delete(self, method: ClassMethod[T, None]):
        self.deleter = method
        return self

    def __get__(self, instance, owner):
        return self.getter(owner)

    def __set__(self, instance, value):
        self.setter(value)

    def __delete__(self, instance):
        self.deleter()

def abstract_const():
    return type("ABSTRACT_CONST", (object,), {"__isabstractmethod__": True})()

def iterate_date(start: dt.date, end: dt.date):
    current = start
    while current <= end:
        yield current
        current += dt.timedelta(days=1)

class Market(ABC):
    cache: Cache

    def __init_subclass__(cls) -> None:
        cls.cache = Cache()

    name = abstract_const()
    country = abstract_const()
    include_country_holidays = abstract_const()
    excluded_country_holidays = abstract_const()

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
    @abstractmethod
    def weekends(cls) -> DAYS_TYPE:
        """
        Return list of integers representing standard non-trading weekend days.
        """
        if hasattr(cls, "_weekends"):
            return cls._weekends
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
    def get_holidays(cls, start: dt.date, end: dt.date) -> list[Holiday]:
        """Return list of holidays between start and end dates."""
        return list(filter(lambda d: isinstance(d, Holiday), [cls.cache.get_or_set(day, cls.fetch_data) for day in iterate_date(start, end)]))

    @classmethod
    def get_partial_days(cls, start: dt.date, end: dt.date) -> list[PartialTradingDay]:
        return list(filter(lambda d: isinstance(d, PartialTradingDay), [cls.cache.get_or_set(day, cls.fetch_data) for day in iterate_date(start, end)]))

    @classmethod
    def get_trading_days(cls, start: dt.date, end: dt.date) -> list[TradingDay]:
        """Return list of trading days between start and end dates."""
        return list(filter(lambda d: isinstance(d, TradingDay), [cls.cache.get_or_set(day, cls.fetch_data) for day in iterate_date(start, end)]))

    @classmethod
    def is_weekday(cls, date: dt.date) -> bool:
        return date.weekday() in cls.weekdays

    @classmethod
    def is_weekend(cls, date: dt.date) -> bool:
        return date.weekday() in cls.weekends

    @classmethod
    def is_holiday(cls, date: dt.date) -> bool:
        holidays = cls.get_holidays(date, date)
        return any(holiday.date == date for holiday in holidays)

    @classmethod
    def is_partial_day(cls, date: dt.date) -> bool:
        partial_days = cls.get_partial_days(date, date)
        return any(partial.date == date for partial in partial_days)

    @classmethod
    def is_trading_day(cls, date: dt.date) -> bool:
        if not cls.is_weekday(date):
            return False
        if cls.is_holiday(date):
            return False
        return True

    @classmethod
    def get_trading_day(cls, date: dt.date) -> t.Optional[TradingDay]:
        if not cls.is_trading_day(date):
            return None
        else:
            return cls.cache.get_or_set(date, cls.fetch_data)

    @classmethod
    def day(cls, date: dt.date) -> Day:
        return cls.cache.get_or_set(date, cls.fetch_data)