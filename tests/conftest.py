import logging
import warnings

import dagster
import pytest
from _pytest.tmpdir import TempPathFactory
from dagster import DagsterInstance

logging.getLogger("alembic.runtime.migration").setLevel(logging.WARNING)
warnings.filterwarnings("ignore", category=dagster.ExperimentalWarning)


@pytest.fixture
def dagster_instance(tmp_path_factory: TempPathFactory) -> DagsterInstance:
    return DagsterInstance.ephemeral(tempdir=str(tmp_path_factory.mktemp("dagster_home")))


@pytest.fixture(scope="session")
def session_scoped_dagster_instance(tmp_path_factory: TempPathFactory) -> DagsterInstance:
    return DagsterInstance.ephemeral(tempdir=str(tmp_path_factory.mktemp("dagster_home_session")))
