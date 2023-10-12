from dataclasses import dataclass
from string import printable
from typing import Any, Dict, List, Optional

from dagster import asset, materialize
from hypothesis import given, settings
from hypothesis.strategies import booleans, dictionaries, floats, integers, lists, recursive, text
from serde.yaml import from_yaml
from upath import UPath

from dagster_serde.io_managers.yaml import YamlIOManager
from tests.utils import get_saved_path

json = recursive(
    booleans()
    | integers(min_value=-(2**63) + 1, max_value=2**64 - 1)
    | floats(allow_infinity=False, allow_nan=False)
    | text(printable),
    lambda children: lists(children) | dictionaries(text(printable), children),
)


@given(data=json)
@settings(max_examples=100, deadline=None)  # type: ignore
def test_yaml_io_manager_untyped(tmpdir_factory, data: Any):
    io_manager = YamlIOManager(base_dir=str(tmpdir_factory.mktemp("yaml")))

    @asset(io_manager_def=io_manager)
    def upstream() -> Any:
        return data

    @asset(io_manager_def=io_manager)
    def downstream(upstream: Any) -> None:
        assert upstream == data

    materialize(
        [upstream, downstream],
    )


def test_yaml_io_manager_typed(tmpdir_factory):
    io_manager = YamlIOManager(base_dir=str(tmpdir_factory.mktemp("json")))

    @dataclass
    class MyStruct:
        a: str
        b: int
        c: float
        d: bool
        e: List[str]
        f: Dict[str, int]
        g: Optional[str]

    my_struct = MyStruct(
        a="hello",
        b=1,
        c=1.0,
        d=True,
        e=["hello", "world"],
        f={"hello": 1, "world": 2},
        g=None,
    )

    @asset(io_manager_def=io_manager)
    def upstream() -> MyStruct:
        return my_struct

    @asset(io_manager_def=io_manager)
    def downstream(upstream: MyStruct) -> None:
        assert isinstance(upstream, MyStruct)
        assert upstream == my_struct

    result = materialize(
        [upstream, downstream],
    )
    saved_path = get_saved_path(result, "upstream")
    assert saved_path.endswith(".yaml")
    assert from_yaml(MyStruct, UPath(saved_path).read_text()) == my_struct
