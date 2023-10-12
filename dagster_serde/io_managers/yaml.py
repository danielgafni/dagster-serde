from typing import Any

import yaml
from serde.yaml import from_yaml, to_yaml

from dagster_serde.io_managers.base import BaseSerdeUPathIOManager


class YamlIOManager(BaseSerdeUPathIOManager):
    extension: str = ".yaml"

    def serialize_dataclass(self, obj: Any, cls: Any) -> str:
        return to_yaml(obj, cls=cls)

    def deserialize_dataclass(self, data: str, cls: Any) -> Any:
        return from_yaml(cls, data)

    def serialize_object(self, obj: Any) -> str:
        return yaml.safe_dump(obj)

    def deserialize_object(self, data: str) -> Any:
        return yaml.safe_load(data)
