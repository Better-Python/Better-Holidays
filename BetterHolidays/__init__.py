from .days import Day, Holiday, TradingDay, PartialTradingDay
from .markets import MARKETS, NYSE, Market

def get_market(name: str) -> 'type[Market]':
    return MARKETS[name]
