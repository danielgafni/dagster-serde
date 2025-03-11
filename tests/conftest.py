import logging
from typing import Type

import pytest
import pytest_cases
from _pytest.tmpdir import TempPathFactory
from dagster import DagsterInstance

from dagster_serde import BaseSerdeUPathIOManager, JsonIOManager, YamlIOManager
from tests.data import MyDataclass, MyInnerDataclass

logging.getLogger("alembic.runtime.migration").setLevel(logging.WARNING)


@pytest.fixture
def dagster_instance(tmp_path_factory: TempPathFactory) -> DagsterInstance:
    return DagsterInstance.ephemeral(tempdir=str(tmp_path_factory.mktemp("dagster_home")))


@pytest.fixture(scope="session")
def session_scoped_dagster_instance(tmp_path_factory: TempPathFactory) -> DagsterInstance:
    return DagsterInstance.ephemeral(tempdir=str(tmp_path_factory.mktemp("dagster_home_session")))


@pytest.fixture
def my_dataclass() -> MyDataclass:
    return MyDataclass(
        a="hello",
        b=1,
        c=1.0,
        d=True,
        e=["hello", "world"],
        f={"hello": 1, "world": 2},
        g=None,
        h=MyInnerDataclass(foo="bar"),
        i=[MyInnerDataclass(foo="bar"), MyInnerDataclass(foo="baz")],
        j={"hello": MyInnerDataclass(foo="bar"), "world": MyInnerDataclass(foo="baz")},
    )


@pytest_cases.fixture  # type: ignore
@pytest.mark.parametrize(
    "klass",
    [
        JsonIOManager,
        YamlIOManager,
    ],
)
def serde_io_manager(tmpdir_factory, klass: Type[BaseSerdeUPathIOManager]) -> BaseSerdeUPathIOManager:
    return klass(base_dir=str(tmpdir_factory.mktemp(str(klass.__name__))))
