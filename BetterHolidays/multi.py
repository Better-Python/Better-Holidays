# Standalone functions like in utils.py but are exported

import typing as t
from .utils import NOT_SET
from .markets import MARKETS, Market

T = t.TypeVar("T", bound=t.Any)

@t.overload
def get_market(name:'str') -> 'type[Market]': ...

@t.overload
def get_market(name:'str', default:'T') -> 't.Union[T, type[Market]]': ...

def get_market(name, default=NOT_SET):
    if name in MARKETS:
        return MARKETS[name]
    
    if default == NOT_SET:
        raise KeyError(name)
    
    return default