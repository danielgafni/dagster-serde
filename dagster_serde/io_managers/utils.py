from dataclasses import is_dataclass
from functools import wraps
from typing import Any, Callable, Mapping, TypeAlias, Union, get_args, get_origin

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


@unwrap_optional
def annotation_is_pydantic_model(annotation: Any) -> bool:
    from pydantic import BaseModel

    return issubclass(annotation, BaseModel)
