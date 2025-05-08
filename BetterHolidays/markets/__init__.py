from .market import Market

from .nyse import NYSE
from .nasdaq import NASDAQ
from .sse import SSE
from .lse import LSE

MARKETS: "dict[str, type[Market]]" = {
    "NYSE": NYSE,
    "NASDAQ": NASDAQ,
    "SSE": SSE,
    "LSE": LSE,
}

__all__ = ["MARKETS", "Market", "NYSE", "NASDAQ", "SSE", "LSE"]
