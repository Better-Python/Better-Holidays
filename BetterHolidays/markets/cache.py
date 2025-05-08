import datetime as dt
import typing as t
from ..days import Day
from ..utils import NOT_SET, get_db
import peewee as pw

T = t.TypeVar("T")

DB = get_db()


class Cache:
    def __init__(self, market:'str'):
        self.market = market

    def get(self, key: "dt.date") -> "Day":
        return Day.select().where(Day.date == key, Day.market == self.market).get()

    def set(self, day: "Day"):
        day.market.db_value(self.market)
        day.save()

    def get_or_set(self, key: "dt.date", func: "t.Callable[[int], None]") -> "Day":
        try:
            return self.get(key)
        except pw.DoesNotExist:
            func(key.year)

        try:
            return self.get(key)
        except pw.DoesNotExist:
            raise ValueError(f"Could not find day {key} after fetching data")

    def clear(self):
        Day.delete().where(Day.market == self.market).execute()


    @t.overload
    def pop(self, key: "dt.date") -> "Day": ...

    @t.overload
    def pop(self, key: "dt.date", default: "T") -> "t.Union[Day, T]": ...

    def pop(self, key, default=NOT_SET):
        try:
            if default == NOT_SET:
                try:
                    item = Day.select().where(Day.market == self.market, Day.date == key).get()
                    if item:
                        item.delete_instance()
                        return item
                except:
                    raise KeyError(key)

            try:
                item = Day.select().where(Day.market == self.market, Day.date == key).get()
                if item:
                    return item
            except:
                return default

        except KeyError:
            raise
        except Exception as e:
            raise KeyError(key)

    def __contains__(self, key: "dt.date") -> bool:
        return key in Day.select().where(Day.market == self.market, Day.date == key).get()
