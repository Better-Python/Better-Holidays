import typing as t

DAYS = (
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
    "SATURDAY",
    "SUNDAY"
)

DAYS_MAP = {day: i for i, day in enumerate(DAYS)}
MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = 0,1,2,3,4,5,6
DAYS_TYPE = t.Literal[0,1,2,3,4,5,6]

MONTHS = (
    "JANUARY",
    "FEBRUARY",
    "MARCH",
    "APRIL",
    "MAY",
    "JUNE",
    "JULY",
    "AUGUST",
    "SEPTEMBER",
    "OCTOBER",
    "NOVEMBER",
    "DECEMBER"
)
MONTHS_MAP = {month: i for i, month in enumerate(MONTHS, 1)}

JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER = range(12)


DAYS_IN_MONTH = {
    "JANUARY": 31,
    "FEBRUARY": 28,
    "MARCH": 31,
    "APRIL": 30,
    "MAY": 31,
    "JUNE": 30,
    "JULY": 31,
    "AUGUST": 31,
    "SEPTEMBER": 30,
    "OCTOBER": 31,
    "NOVEMBER": 30,
    "DECEMBER": 31
}

