from typing import (
    TypeVar,
)

_T = TypeVar('_T')

_VariableConfig = tuple[str, _T, type[_T]]
