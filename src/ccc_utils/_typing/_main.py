from typing import (
    Any,
    Callable,
    TypedDict,
    TypeVar,
)
import pandas as pd
from pandas._typing import AstypeArg

class Dtypes(TypedDict):
    index: str
    dtype: AstypeArg

_T = TypeVar('_T')

SeriesApply = Callable[[_T], Any]

SeriesPipe = Callable[[pd.Series], pd.Series]

ParsingMap = dict[AstypeArg, SeriesPipe]
