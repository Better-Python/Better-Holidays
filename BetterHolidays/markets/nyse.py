import BetterMD as md
from BetterMD import elements as elm
from .market import Market, classproperty
from .holidays import NewYearsDay, MartinLutherKingJrDay, WashingtonsBirthday, GoodFriday, MemorialDay, JuneteenthNationalIndependenceDay, IndependenceDay, LaborDay, Thanksgiving, Christmas, CommonHoliday
from ..days import Day, Holiday, TradingDay, PartialTradingDay, NonTradingDay
from ..const import MONTHS_MAP
import datetime as dt

# Standard open/close times = 9:30 - 4:00
# * Close at 1pm
# ** Closes at 1pm
# *** Closes at 1pm

def iter_days(start: dt.date, end: dt.date):
    current = start
    while current <= end:
        yield current
        current += dt.timedelta(days=1)

def iter_year(year: int):
    start = dt.date(year, 1, 1)
    end = dt.date(year, 12, 31)
    return iter_days(start, end)

class NYSE(Market):
  name = "NYSE"
  country = "US"
  include_country_holidays = True
  excluded_country_holidays = []

  abnormal_days: 'dict[dt.date, Day]' = {}

  standard_open_time = dt.time(hour=9, minute=30)
  standard_close_time = dt.time(hour=16)

  holidays:'list[CommonHoliday]' = [
      NewYearsDay([0,1,2,3,4], change={6: 1, 5: -1} ), # Saturday -> Friday, Sunday -> Monday
      MartinLutherKingJrDay([0,1,2,3,4], change={6: 1, 5: -1} ),
      WashingtonsBirthday([0,1,2,3,4], change={6: 1, 5: -1} ),
      GoodFriday([0,1,2,3,4], change={6: 1, 5: -1} ),
      MemorialDay([0,1,2,3,4], change={6: 1, 5: -1} ),
      JuneteenthNationalIndependenceDay([0,1,2,3,4], change={6: 1, 5: -1} ),
      IndependenceDay([0,1,2,3,4], change={6: 1, 5: -1} ),
      LaborDay([0,1,2,3,4], change={6: 1, 5: -1} ),
      Thanksgiving([0,1,2,3,4], change={6: 1, 5: -1} ),
      Christmas([0,1,2,3,4], change={6: 1, 5: -1} )
  ]


  @classproperty
  def weekdays(cls):
     return [0,1,2,3,4]

  @classmethod
  def fetch_data(cls, year: 'int'):
     if year < dt.date.today().year:
        return cls.fetch_past(year)
     else:
        return cls.fetch_future()

  @classmethod
  def fetch_past(cls, year: 'int'):
      yr = {}

      for holiday in cls.holidays:
         d = holiday(year)
         if d is None:
            continue
         yr[d.date] = d

      for day in iter_year(year):
          if day in yr:
              cls.cache.set(day, yr[day])
          elif day in cls.abnormal_days:
            cls.cache.set(day, cls.abnormal_days[day])
          elif day.weekday() in cls.weekdays:
            cls.cache.set(day, TradingDay(date=day, open_time=cls.standard_open_time, close_time=cls.standard_close_time))
          else:
            cls.cache.set(day, NonTradingDay(date=day))

  @classmethod
  def get_day_type(cls, day: dt.date) -> type[Day]:
     if day in cls.abnormal_days:
        return cls.abnormal_days[day]
     
     elif day in cls.weekdays:
        return TradingDay
     else:
        return NonTradingDay
  
  @classmethod
  def fetch_future(cls):
    doc = md.HTML.from_url("https://www.nyse.com/markets/hours-calendars")
    table:'elm.Table' = doc.inner_html.get_elements_by_class_name("table-data")[0]

    table_dict = table.to_dict()
    holidays = table_dict.pop("Holiday")

    for year, dates in table_dict.items():
      def handle_date(date:'str'):
          split_date = date.split(" ")
          
          return dt.date(int(year), int(MONTHS_MAP[split_date[1].upper()]), int(split_date[2].replace("*", "")))
      
      hol_dates = {handle_date(date): hol for date, hol in zip(dates, holidays)}

      for day in iter_year(int(year)):
        if day in hol_dates:
          name = hol_dates[day]
          if name.endswith("*"):
            cls.cache.set(
              day,
              PartialTradingDay(
                date=day,
                open_time=dt.time(hour=9, minute=30),
                close_time=dt.time(hour=13),
                early_close=True,
                early_close_reason=name.removesuffix("*")
              )
            )
          else:
             cls.cache.set(
              day,
              Holiday(
                date=day,
                name=name
              )
            )
        elif day.weekday() in cls.weekdays:
          cls.cache.set(
            day,
            TradingDay(
              date=day,
              open_time=cls.standard_open_time,
              close_time=cls.standard_close_time
            )
          )
        else:
          cls.cache.set(day, Day(date=day))