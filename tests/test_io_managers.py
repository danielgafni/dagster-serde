from typing import Any

from dagster import asset, materialize
from hypothesis import HealthCheck, given, settings

from dagster_serde.io_managers.base import BaseSerdeUPathIOManager
from tests.data import MyDataclass
from tests.strategies import json_like


@given(data=json_like)
@settings(max_examples=100, deadline=None, suppress_health_check=list(HealthCheck))  # type: ignore
def test_io_manager_untyped(data: Any, serde_io_manager: BaseSerdeUPathIOManager):
    @asset(io_manager_def=serde_io_manager)
    def upstream() -> Any:
        return data

    @asset(io_manager_def=serde_io_manager)
    def downstream(upstream: Any) -> None:
        assert upstream == data

    materialize(
        [upstream, downstream],
    )


def test_io_manager_typed(my_dataclass: MyDataclass, serde_io_manager: BaseSerdeUPathIOManager):
    @asset(io_manager_def=serde_io_manager)
    def upstream() -> MyDataclass:
        return my_dataclass

    @asset(io_manager_def=serde_io_manager)
    def downstream(upstream: MyDataclass) -> None:
        assert isinstance(upstream, MyDataclass)
        assert upstream == my_dataclass

    materialize(
        [upstream, downstream],
    )
