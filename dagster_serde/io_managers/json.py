from typing import Any

import orjson
from serde.json import from_json, to_json

from dagster_serde.io_managers.base import BaseSerdeUPathIOManager


class JsonIOManager(BaseSerdeUPathIOManager):
    def serialize_dataclass(self, obj: Any, cls: Any) -> str:
        return to_json(obj, cls=cls)

    def deserialize_dataclass(self, data: str, cls: Any) -> Any:
        return from_json(cls, data)

    def serialize_object(self, obj: Any) -> str:
        return orjson.dumps(obj).decode()

    def deserialize_object(self, data: str) -> Any:
        return orjson.loads(data.encode())
