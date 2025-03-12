from string import printable

from hypothesis.strategies import booleans, dictionaries, floats, integers, lists, recursive, text

json_like = recursive(
    booleans()
    | integers(min_value=-(2**63) + 1, max_value=2**64 - 1)
    | floats(allow_infinity=False, allow_nan=False)
    | text(printable),
    lambda children: lists(children) | dictionaries(text(printable), children),
)
