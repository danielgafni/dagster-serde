

# `dagster-serde`

[![image](https://img.shields.io/pypi/v/dagster-serde.svg)](https://pypi.python.org/pypi/dagster-serde)
[![image](https://img.shields.io/pypi/l/dagster-serde.svg)](https://pypi.python.org/pypi/dagster-serde)
[![image](https://img.shields.io/pypi/pyversions/dagster-serde.svg)](https://pypi.python.org/pypi/dagster-serde)
[![CI](https://github.com/danielgafni/dagster-serde/actions/workflows/ci.yml/badge.svg)](https://github.com/danielgafni/dagster-serde/actions/workflows/ci.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Type-aware ser/de library for [Dagster](https://github.com/dagster-io/dagster).

```python
@dataclass
class MyStruct:
    foo: str


my_struct = MyStruct(foo="bar")


@asset(
    io_manager_key="json_io_manager",
)
def upstream() -> MyStruct:
    return my_struct  # my_struct is serialized to a json file (type hint is optional)


@asset
def downstream(
    upstream: MyStruct,
):  # my_struct is loaded as MyStruct based on the type hint
    assert upstream == my_struct
```

# Installation

```shell
pip install dagster-serde
```

List of available extras:
 - `json`
 - `yaml`

For example, to use the `JsonIOManager`, install `dagster-serde[json]`.

# IOManagers

## `BaseSerdeUPathIOManager`
Base class for IOManagers that ser/de to/from filesystems.

- Automatically deserializes inputs based on type annotations. If the input annotation is not a supported type, it's returned as a normal built-in type (e.g. `str`, `int`, `dict`, etc.). The supported types are:
  - `dataclasses.dataclass` and `serde.serde` (using `pyserde`). The full list of supported types can be found [here](https://github.com/yukinarit/pyserde#features).
  - TODO: add support for other libraries like `pydantic`

- `Optional` type annotations are supported. If the input annotation is `Optional` and is missing in the filesystem, the `IOManager` will skip loading the input and return `None` instead. If the output annotation is `Optional` and the output is `None`, the `IOManager` will skip writing the output to the filesystem.


## `JsonIOManager`

Implements `BaseSerdeUPathIOManager` for JSON files. Uses `orjson`.


## `YamlIOManager`

Implements `BaseSerdeUPathIOManager` for YAML files. Uses `pyyaml`.

# Examples
See [examples](docs/examples.md).

## Development

### Installation
```shell
poetry install
poetry run pre-commit install
```

### Testing
```shell
poetry run pytest
```
