
# Examples

## Providing IOManagers to `Definitions`

```python
from dagster import Definitions
from dagster_serde import JsonIOManager

base_dir = (
    "/remote/or/local/path"  # s3://my-bucket/... or gs://my-bucket/... also works!
)

definitions = Definitions(
    resources={
        "json_io_manager": JsonIOManager(base_dir=base_dir),
    }
)
```

## Ser/de of dataclasses


```python
from dataclasses import dataclass
from dagster import asset, Definitions
from dagster_serde import JsonIOManager

base_dir = (
    "/remote/or/local/path"  # s3://my-bucket/... or gs://my-bucket/... also works!
)


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


@asset(
    io_manager_key="json_io_manager",
)
def upstream() -> MyStruct:
    return my_struct


@asset
def downstream(upstream: MyStruct):
    assert upstream == my_struct
```
