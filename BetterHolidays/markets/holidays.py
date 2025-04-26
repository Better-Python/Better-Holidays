import datetime as dt
from ..days import Day, Holiday, PartialTradingDay
import BetterMD as md
from ..const import MONTHS_MAP, DAYS_TYPE, MONDAY, THURSDAY

def next_day(day: 'DAYS_TYPE', want:'DAYS_TYPE') -> 'DAYS_TYPE':
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
        return (7-day)+want
    return want-day

class CommonHoliday:
    name: 'str'
    month: 'int' = None
    day: 'int' = None
    type: 'type[Day]' = Holiday

    open_time: 'dt.time' = None
    close_time: 'dt.time' = None
    early_close: 'bool' = False
    late_open: 'bool' = False
    holiday_reason: 'str' = ""

    def __init__(self, days:'list[int]', change:'dict[int, int]', start: dt.date = None, end: dt.date = None):
        """
        Args:
            days: What days this holiday is on
            change: What happens if the holiday falls on a weekend
        """
        self.days = days
        self.change = change
        self.start = start
        self.end = end

    def get_date(self, year: 'int'):
        return dt.date(year, self.month, self.day)

    def __call__(self, year: 'int'):          
        day = self.get_date(year)
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
                late_open_reason=self.holiday_reason
            )

        return None

class NewYearsDay(CommonHoliday):
    name = "New Year's Day"
    month = 1
    day = 1

class MartinLutherKingJrDay(CommonHoliday):
    """
    3rd Monday in January
    """
    name = "Martin Luther King Jr. Day"

    def get_date(self, year: 'int'):
        jan21 = dt.date(year, 1, 21)
        return jan21+dt.timedelta(days=(next_day(jan21.weekday(), MONDAY)))


class WashingtonsBirthday(CommonHoliday):
    """
    3rd Monday in February
    """
    name = "Washington's Birthday"

    def get_date(self, year: 'int'):
        feb15 = dt.date(year, 2, 15)
        return feb15+dt.timedelta(days=next_day(feb15.weekday(), MONDAY))

class GoodFriday(CommonHoliday):
    """
    See website for day
    """
    name = "Good Friday"

    def get_date(self, year: int) -> dt.date:
        try:
            url = f"https://www.officesimplify.com/bank-holidays-uk-{year}"
            html = md.HTML.from_url(url)
            elements = html.inner_html.advanced_find("td", attrs={"text": "Good Friday"})
            if not elements:
                raise ValueError(f"Could not find Good Friday information for {year}")
            tr = elements[0].parent
            day, month = tr.children[0].text.split(" ")
            return dt.date(year, MONTHS_MAP[month], int(day[:-2]))
        except Exception as e:  
            raise ValueError(f"Error determining Good Friday date for {year}: {str(e)}")  

class MemorialDay(CommonHoliday):
    """
    Last Monday in May
    """
    name = "Memorial Day"

    def get_date(self, year: 'int'):
        may31 = dt.date(year, 5, 31).weekday()
        return dt.date(year, 5, 31-may31)

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

    def get_date(self, year: 'int'):
        sept1 = dt.date(year, 9, 1)
        return sept1+dt.timedelta(days=next_day(sept1.weekday(), MONDAY))

class Thanksgiving(CommonHoliday):
    """
    4th Thursday in November
    """
    name = "Thanksgiving"

    def get_date(self, year: 'int'):
        nov25 = dt.date(year, 11, 25)
        return nov25+dt.timedelta(days=next_day(nov25.weekday(), THURSDAY))

class Christmas(CommonHoliday):
    name = "Christmas"
    month = 12
    day = 25
