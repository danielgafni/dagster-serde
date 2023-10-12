from abc import abstractmethod
from dataclasses import is_dataclass
from functools import wraps
from typing import Any, Callable, Dict, Mapping, Optional, Union, get_args, get_origin

from dagster import (
    ConfigurableIOManager,
    InitResourceContext,
    InputContext,
    MetadataValue,
    OutputContext,
    UPathIOManager,
)
from dagster import _check as check
from pydantic.fields import Field, PrivateAttr
from typing_extensions import TypeAlias
from upath import UPath

Partitions: TypeAlias = Mapping


def annotation_is_typing_optional(annotation: Any) -> bool:
    return get_origin(annotation) == Union and type(None) in get_args(annotation)


def unwrap_optional(
    condition: Callable[
        [
            Any,
        ],
        bool,
    ]
):
    @wraps(condition)
    def inner(annotation: Any):
        if not annotation_is_typing_optional(annotation):
            return condition(annotation)
        else:
            inner_annotation = get_args(annotation)[0]
            return condition(inner_annotation)

    return inner


@unwrap_optional
def annotation_is_dataclass(annotation: Any) -> bool:
    return is_dataclass(annotation)


class BaseSerdeUPathIOManager(ConfigurableIOManager, UPathIOManager):
    # This is a base class which doesn't define the specific format (parquet, csv, etc) to use
    """
    `IOManager` for `serde` based on the `UPathIOManager`.
    Features:
     - returns the correct @serde class based on the type annotation
     - handles `Optional` types by skipping loading missing inputs or `None` outputs
     - inherits all the features of the `UPathIOManager` - works with local and remote filesystems (like S3),
         supports loading multiple partitions, ...
    """

    base_dir: Optional[str] = Field(default=None, description="Base directory for storing files.")

    _base_path: UPath = PrivateAttr()

    def setup_for_execution(self, context: InitResourceContext) -> None:
        self._base_path = (
            UPath(self.base_dir)
            if self.base_dir is not None
            else UPath(check.not_none(context.instance).storage_directory())
        )

    @abstractmethod
    def serialize_dataclass(self, obj: Any, cls: Any) -> str:
        ...

    @abstractmethod
    def deserialize_dataclass(self, s: str, cls: Any) -> Any:
        ...

    @abstractmethod
    def serialize_object(self, obj: Any) -> str:
        ...

    @abstractmethod
    def deserialize_object(self, s: str) -> Any:
        ...

    def dump_to_path(
        self,
        context: OutputContext,
        obj: Any,
        path: UPath,
    ):
        if annotation_is_typing_optional(context.dagster_type.typing_type) and (obj is None):
            context.log.warning(self.get_optional_output_none_log_message(context, path))
            return
        else:
            assert obj is not None, "output should not be None if it's type annotation is not Optional"
            if annotation_is_dataclass(context.dagster_type.typing_type) and is_dataclass(object):
                string = self.serialize_dataclass(obj, context.dagster_type.typing_type)
            elif is_dataclass(obj):
                string = self.serialize_dataclass(obj, type(obj))
            else:
                string = self.serialize_object(obj)
            path.write_text(string)

    def load_from_path(self, path: UPath, context: InputContext) -> Any:
        if annotation_is_typing_optional(context.dagster_type.typing_type) and not path.exists():
            context.log.warning(self.get_missing_optional_input_log_message(context, path))
            return None

        string = path.read_text()

        if annotation_is_dataclass(context.dagster_type.typing_type):
            return self.deserialize_dataclass(string, context.dagster_type.typing_type)
        else:
            return self.deserialize_object(string)

    def get_metadata(self, context: OutputContext, obj: Any) -> Dict[str, MetadataValue]:
        if obj is None:
            return {"missing": MetadataValue.bool(True)}
        else:
            return {}

    @staticmethod
    def get_storage_options(path: UPath) -> dict:
        storage_options = {}

        try:
            storage_options.update(path._kwargs.copy())
        except AttributeError:
            pass

        return storage_options

    def get_missing_optional_input_log_message(self, context: InputContext, path: UPath) -> str:
        return f"Optional input {context.name} at {path} doesn't exist in the filesystem and won't be loaded!"

    def get_optional_output_none_log_message(self, context: OutputContext, path: UPath) -> str:
        return f"The object for the optional output {context.name} is None, so it won't be saved to {path}!"
