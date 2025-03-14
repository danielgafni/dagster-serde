from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class MyInnerDataclass:
    foo: str


@dataclass
class MyDataclass:
    a: str
    b: int
    c: float
    d: bool
    e: List[str]
    f: Dict[str, int]
    g: Optional[str]
    h: MyInnerDataclass
    i: List[MyInnerDataclass]
    j: Dict[str, MyInnerDataclass]
