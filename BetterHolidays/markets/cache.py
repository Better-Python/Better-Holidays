import datetime as dt
import typing as t
from ..days import Day
from ..utils import NOT_SET

T = t.TypeVar("T")

class Cache:
    def __init__(self):
        self.cache: 'dict[dt.date, Day]' = {}

    def get(self, key: 'dt.date') -> 't.Optional[Day]':
        return self.cache.get(key)

    def set(self, key: 'dt.date', value: 'Day'):
        self.cache[key] = value

    def get_or_set(self, key: 'dt.date', func: 't.Callable[[int], None]') -> 'Day':
        if key in self.cache:
            return self.get(key)
        func(key.year)
        if key in self.cache:
            return self.get(key)
        raise ValueError("Cache miss")

    def clear(self):
        self.cache.clear()

    @t.overload
    def pop(self, key:'dt.date') -> 'Day': ...

    @t.overload
    def pop(self, key:'dt.date', default:'T') -> 't.Union[Day, T]': ...

    def pop(self, key, default=NOT_SET):
        if default == NOT_SET:     
            return self.cache.pop(key)

        return self.cache.pop(key, default)

    def __contains__(self, key: 'dt.date') -> bool:
        return key in self.cache