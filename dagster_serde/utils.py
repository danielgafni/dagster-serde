from collections.abc import Mapping, Sequence
from typing import Any

import dagster as dg
from dagster._config.field_utils import IntEnvVar


def _process_dagster_env_vars(config: Any) -> Any:
    # If it's already one of the EnvVar types, return its value
    if isinstance(config, (dg.EnvVar, IntEnvVar)):
        return config.get_value()

    # If it's exactly {"env": "FOO"}, fetch the value
    if isinstance(config, Mapping) and len(config) == 1 and "env" in config:
        return dg.EnvVar(config["env"]).get_value()

    # If it's a dictionary, recurse into its values
    if isinstance(config, Mapping):
        return {k: _process_dagster_env_vars(v) for k, v in config.items()}

    # If it's a list/tuple, recurse into each element
    if isinstance(config, Sequence) and not isinstance(config, str):
        return [_process_dagster_env_vars(v) for v in config]

    # Otherwise, just return as-is
    return config
