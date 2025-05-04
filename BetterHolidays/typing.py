import typing as t

T = t.TypeVar("T")
T1 = t.TypeVar("T1")

ClassMethod = t.Callable[[T], T1]
