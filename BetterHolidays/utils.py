from .markets import MARKETS, Market
import functools as ft
import datetime as dt
from .typing import ClassMethod

import typing as t

T = t.TypeVar('T')
T1 = t.TypeVar('T1')
T2 = t.TypeVar("T2", bound=t.Any)

NOT_SET = type("NOT_SET", (object,), {})

def not_set(type_: str, attr: str):
    raise AttributeError(f"Can't {type_} attribute {attr}")

@t.overload
def get_market(name:'str') -> 'type[Market]': ...

@t.overload
def get_market(name:'str', default:'T2') -> 't.Union[T2, type[Market]]': ...

def get_market(name, default=NOT_SET):
    if name in MARKETS:
        return MARKETS[name]
    
    if default == NOT_SET:
        raise KeyError(name)
    
    return default

def method_cache(cache_method: t.Callable[[], T1]):
    def wrapper(func: t.Callable[[T], T1]):
        cache = cache_method()
        @ft.wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs, cache=cache)
        return inner
    return wrapper

class classproperty(t.Generic[T, T1]):
    def __init__(self, getter: ClassMethod[T, T1]):
        self.getter = getter
        self.setter = lambda val: not_set("set", self.getter.__name__)
        self.deleter = lambda: not_set("delete", self.getter.__name__)

    def set(self, method: 'ClassMethod[T, None]'):
        self.setter = method
        return self

    def delete(self, method: 'ClassMethod[T, None]'):
        self.deleter = method
        return self

    def __get__(self, instance, owner):
        return self.getter(owner)

    def __set__(self, instance, value):
        self.setter(value)

    def __delete__(self, instance):
        self.deleter()

@method_cache(lambda: {"type": type("ABSTRACT_CONST", (object,), {"__isabstractmethod__": True})})
def abstract_const(cache):
    return cache["type"]()

def iterate_date(start: 'dt.date', end: 'dt.date'):
    current = start
    while current <= end:
        yield current
        current += dt.timedelta(days=1)


