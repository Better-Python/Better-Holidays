import functools as ft
import datetime as dt
from .typing import ClassMethod
import platformdirs as pd
import peewee as pw
import os

import typing as t

T = t.TypeVar("T")
T1 = t.TypeVar("T1")
T2 = t.TypeVar("T2", bound=t.Any)
T3 = t.TypeVar("T3")
T4 = t.TypeVar("T4")

NOT_SET = type("NOT_SET", (object,), {})
PATH_TO_DB = pd.user_cache_dir("betterhollidays", "Better-Python")


def not_set(type_: str, attr: str):
    raise AttributeError(f"Can't {type_} attribute {attr}")


def method_cache(cache_method: t.Callable[[], T1]):
    def wrapper(func: t.Callable[[T3 | T1], T4]):
        cache = cache_method()

        @ft.wraps(func)
        def inner(*args, **kwargs) -> "T4":
            return func(*args, **kwargs, cache=cache)

        return inner

    return wrapper


@method_cache(
    lambda: {"db": pw.SqliteDatabase(os.path.join(PATH_TO_DB, "holidays.db"))}
)
def get_db(cache) -> pw.SqliteDatabase:
    return cache["db"]


class classproperty(t.Generic[T, T1]):
    def __init__(self, getter: ClassMethod[T, T1]):
        self.getter = getter
        self.setter = lambda val: not_set("set", self.getter.__name__)
        self.deleter = lambda: not_set("delete", self.getter.__name__)

    def set(self, method: "ClassMethod[T, None]"):
        self.setter = method
        return self

    def delete(self, method: "ClassMethod[T, None]"):
        self.deleter = method
        return self

    def __get__(self, instance, owner):
        return self.getter(owner)

    def __set__(self, instance, value):
        self.setter(value)

    def __delete__(self, instance):
        self.deleter()


@method_cache(
    lambda: {"type": type("ABSTRACT_CONST", (object,), {"__isabstractmethod__": True})}
)
def abstract_const(cache):
    return cache["type"]()


def iterate_date(start: "dt.date", end: "dt.date"):
    current = start
    while current <= end:
        yield current
        current += dt.timedelta(days=1)

def iter_year(year: int):
    start = dt.date(year, 1, 1)
    end = dt.date(year, 12, 31)
    return iterate_date(start, end)

def flatten_list(l:'list[list[T]|T1]', recursive:bool=False) -> 'list[T1|T]':
    ret = []
    for item in l:
        if isinstance(item, list):
            if recursive:
                ret.extend(flatten_list(item, recursive))
            else:
                ret.extend(item)
        else:
            ret.append(item)
    return ret

def default(type_: type[T]) -> T:
    return type_()