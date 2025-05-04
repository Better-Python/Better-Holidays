# Better Markets

A better way to get market holidays

## Installation

```bash
pip install better-holidays
```

## Usage

```python
import BetterHolidays as bh
import datetime as dt

NYSE = bh.get_market("NYSE")
# or
NYSE = bh.NYSE()
print(NYSE.is_holiday(dt.date(1979, 4, 13)))
print(NYSE.is_trading_day(dt.date(1979, 4, 13)))
print(NYSE.is_partial_day(dt.date(1979, 4, 13)))
print(NYSE.is_weekday(dt.date(1979, 4, 13)))
print(NYSE.is_weekend(dt.date(1979, 4, 13)))
print(NYSE.get_holidays(dt.date(1979, 4, 1), dt.date(1979, 4, 30)))
```

## Contributing

Pull requests are welcome.