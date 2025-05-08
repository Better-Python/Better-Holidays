import datetime as dt
from ..days import Day, Holiday, PartialTradingDay
from ..utils import flatten_list, default
import BetterMD as md
from ..const import MONTHS_MAP, DAYS_TYPE, MONDAY, THURSDAY, SUNDAY
import re
import typing as t

def next_day(day: "DAYS_TYPE", want: "DAYS_TYPE") -> "DAYS_TYPE":
    """
    Args:
        day: current day
        want: day to get

    Returns:
        days until want
    """
    if day == want:
        return 0
    elif want < day:
        return (7 - day) + want
    return want - day


def last_day(day: "DAYS_TYPE", want: "DAYS_TYPE") -> "DAYS_TYPE":
    """
    Args:
        day: current day
        want: day to get

    Returns:
        days until want
    """
    return next_day(day, want)


def next_weekend(day: "DAYS_TYPE") -> "DAYS_TYPE":
    """
    Args:
        day: current day

    Returns:
        days until want
    """
    if day in [5, 6]:
        return min(next_day(day + 1, 5), next_day(day + 1, 6)) + 1
    return next_day(day, 5)


def last_weekend(day: "DAYS_TYPE") -> "DAYS_TYPE":
    """
    Args:
        day: current day

    Returns:
        days until want
    """
    if day in [5, 6]:
        return min(last_day(day - 1, 5), last_day(day - 1, 6)) - 1
    return last_day(day, 6)

class CommonHoliday:
    name: "str"
    month: "int" = None
    day: "int" = None
    type: "type[Day]" = Holiday

    open_time: "dt.time" = None
    close_time: "dt.time" = None
    early_close: "bool" = False
    late_open: "bool" = False
    holiday_reason: "str" = ""

    def __init__(
        self,
        days: "list[int]",
        change: "dict[int, int]",
        start: dt.date = None,
        end: dt.date = None,
    ):
        """
        Args:
            days: What days this holiday is on
            change: What happens if the holiday falls on a weekend
        """
        self.days = days
        self.change = change
        self.start = start
        self.end = end

    def get_date(self, year: "int") -> "t.Union[dt.date, list[dt.date]]":
        return dt.date(year, self.month, self.day)

    def __call__(self, year: "int"):
        day = self.get_date(year)

        def for_day(day):
            if day.weekday() not in self.days:
                if day.weekday() in self.change:
                    day += dt.timedelta(days=self.change[day.weekday()])

            if self.start and day < self.start:
                return None

            if self.end and day > self.end:
                return None

            if issubclass(self.type, Holiday):
                return self.type(
                    date=day,
                    name=self.name,
                )

            elif issubclass(self.type, PartialTradingDay):
                return self.type(
                    date=day,
                    open_time=self.open_time,
                    close_time=self.close_time,
                    early_close=self.early_close,
                    late_open=self.late_open,
                    early_close_reason=self.holiday_reason,
                    late_open_reason=self.holiday_reason,
                )

            return None

        if isinstance(day, list):
            return [for_day(d) for d in day]
        return for_day(day)

class ConsistentAbnormalDay(CommonHoliday):
    def __init__(
        self,
        name: "str",
        days: list[int],
        change: dict[int, int],
        month: "int" = None,
        day: "int" = None,
        type: "type[Day]" = Holiday,
        open_time: "dt.time" = None,
        close_time: "dt.time" = None,
        early_close: "bool" = False,
        late_open: "bool" = False,
        holiday_reason: "str" = "",
        start: dt.date = None,
        end: dt.date = None,
    ):
        self.name = name
        self.month = month
        self.day = day
        self.type = type
        self.open_time = open_time
        self.close_time = close_time
        self.early_close = early_close
        self.late_open = late_open
        self.holiday_reason = holiday_reason
        super().__init__(days, change, start, end)


class NewYearsDay(CommonHoliday):
    name = "New Year's Day"
    month = 1
    day = 1


def get_date_from_timeanddate(td: "md.elements.Td", year: "int") -> "dt.date":
    table = td.table
    table_td = table.parent
    table_row: "md.elements.Tr" = table_td.parent
    table_body: "md.elements.TBody" = table_row.parent
    header_row: "md.elements.Tr" = table_body.children[
        table_body.children.index(table_row) - 1
    ]
    header_td: "md.elements.Td" = header_row.children[table_row.index(table_td)]
    month = MONTHS_MAP[header_td.text.strip().upper()]
    day = int(td.text.strip())
    return dt.date(year, month, day)

class ChineseNewYearsDay(CommonHoliday):
    name = "Chinese New Year's Day"

    def get_date(self, year: "int") -> "list[dt.date]":
        page = md.HTML.from_url(
            f"https://www.timeanddate.com/calendar/?year={year}&country=41"
        )
        print(page)
        print(len(page))
        page = page[1]
        cny = [
            get_date_from_timeanddate(td, year)
            for td in page.inner_html.get_by_attr("title", "Chinese New Year")
        ]
        return flatten_list(
            [
                cny[0] - dt.timedelta(last_day(cny[0].weekday(), SUNDAY)),
                cny,
                cny[-1] + dt.timedelta(days=next_weekend(cny[-1].weekday())),
            ]
        )


class ChineseNationalDay(CommonHoliday):
    name = "Chinese National Day"

    def get_date(self, year: int) -> 'dt.date | list[dt.date]':
        page = md.HTML.from_url(
            f"https://www.timeanddate.com/calendar/?year={year}&country=41"
        )
        cnd = page.inner_html.get_by_attr("title", "Chinese National Day")[0]
        cndw = [
            get_date_from_timeanddate(td, year)
            for td in page.inner_html.get_by_attr(
                "title", "National Day Golden Week holiday"
            )
        ]

        return flatten_list(
            [
                cnd - dt.timedelta(last_weekend(cnd.weekday())),
                cnd,
                cndw,
                cndw[-1] + dt.timedelta(days=next_weekend(cndw[-1].weekday())),
            ]
        )


class QingMingFestival(CommonHoliday):
    name = "Qing Ming Jie Festival"

    def get_date(self, year: "int") -> "list[dt.date]":
        page = md.HTML.from_url(
            f"https://www.timeanddate.com/calendar/?year={year}&country=41"
        )
        qmf = [
            get_date_from_timeanddate(td, year)
            for td in page.inner_html.get_by_attr("title", "Qing Ming Jie holiday")
        ]
        return flatten_list(
            [qmf, qmf[-1] + dt.timedelta(days=next_weekend(qmf[-1].weekday()))]
        )


class ChineseLabourDay(CommonHoliday):
    name = "Chinese Labour Day"

    def get_date(self, year: "int") -> "list[dt.date]":
        may1 = dt.date(year, 5, 1)
        return [
            may1 - dt.timedelta(days=last_weekend(may1.weekday())),
            may1,
            dt.date(year, 5, 2),
            dt.date(year, 5, 3),
            dt.date(year, 5, 4),
            dt.date(year, 5, 5),
        ]

class DragonBoatFestival(CommonHoliday):
    name = "Dragon Boat Festival"

    def get_date(self, year: "int") -> "list[dt.date]":
        page = md.HTML.from_url(
            f"https://www.timeanddate.com/calendar/?year={year}&country=41"
        )
        dbf = [
            get_date_from_timeanddate(td, year)
            for td in page.inner_html.get_by_attr("title", "Dragon Boat Festival")
        ]

        return dbf


class AutumnFestival(CommonHoliday):
    name = "Autumn Festival"

    def get_date(self, year: "int") -> "list[dt.date]":
        page = md.HTML.from_url(
            f"https://www.timeanddate.com/calendar/?year={year}&country=41"
        )
        af = [
            get_date_from_timeanddate(td, year)
            for td in page.inner_html.get_by_attr("title", "Autumn Festival")
        ]
        af.insert(0, af[0] - dt.timedelta(last_weekend(af[0].weekday())))
        return af


class MartinLutherKingJrDay(CommonHoliday):
    """
    3rd Monday in January
    """

    name = "Martin Luther King Jr. Day"

    def get_date(self, year: "int"):
        jan21 = dt.date(year, 1, 21)
        return jan21 + dt.timedelta(days=(next_day(jan21.weekday(), MONDAY)))


class WashingtonsBirthday(CommonHoliday):
    """
    3rd Monday in February
    """

    name = "Washington's Birthday"

    def get_date(self, year: "int"):
        feb15 = dt.date(year, 2, 15)
        return feb15 + dt.timedelta(days=next_day(feb15.weekday(), MONDAY))


class LincolnsBirthday(CommonHoliday):
    """
    3rd Monday in February
    """

    name = "Lincolns Birthday"

    month = 2
    day = 12


class GoodFriday(CommonHoliday):
    """
    See website for day
    """

    name = "Good Friday"

    regex = re.compile(r"(\d+) ([a-zA-Z]+) (\d+)")

    def get_date(self, year: "int") -> "dt.date":
        try:
            url = f"https://www.calendar-365.co.uk/holidays/{year}.html"
            try:
                html = md.HTML.from_url(url)
            except Exception as e:
                raise ValueError(f"Better Markdown error: {str(e)}") from e

            try:
                elements = html.inner_html.advanced_find(
                    "a",
                    attrs={
                        "href": "https://www.calendar-365.co.uk/holidays/good-friday.html",
                        "class": "link_arrow",
                        "title": "Good Friday 2026",
                        "text": "Good Friday",
                    },
                )  # The title is 'Good Friday 2026' for all years
                if not elements:
                    raise ValueError(
                        f"Could not find Good Friday information for {year}"
                    )
            except Exception as e:
                raise ValueError(f"Error finding Good Friday information: {str(e)}")

            tr = elements[0].parent.parent
            day, month, _ = self.regex.match(tr.children[0].text).groups()
            return dt.date(year, MONTHS_MAP[month.upper()], int(day))
        except Exception as e:
            raise ValueError(
                f"Error determining Good Friday date for {year}: {str(e)} ({type(e)})"
            )


class MemorialDay(CommonHoliday):
    """
    Last Monday in May
    """

    name = "Memorial Day"

    def get_date(self, year: "int"):
        may31 = dt.date(year, 5, 31).weekday()
        return dt.date(year, 5, 31 - may31)


class JuneteenthNationalIndependenceDay(CommonHoliday):
    name = "Juneteenth National Independence Day"
    month = 6
    day = 19


class IndependenceDay(CommonHoliday):
    name = "Independence Day"
    month = 7
    day = 4


class LaborDay(CommonHoliday):
    """
    1st Monday in September
    """

    name = "Labor Day"

    def get_date(self, year: "int"):
        sept1 = dt.date(year, 9, 1)
        return sept1 + dt.timedelta(days=next_day(sept1.weekday(), MONDAY))


class Thanksgiving(CommonHoliday):
    """
    4th Thursday in November
    """

    name = "Thanksgiving"

    def get_date(self, year: "int"):
        nov25 = dt.date(year, 11, 25)
        return nov25 + dt.timedelta(days=next_day(nov25.weekday(), THURSDAY))


class Christmas(CommonHoliday):
    name = "Christmas"
    month = 12
    day = 25
