from datetime import (
    date,
    timedelta,
)
import pandas as pd
from ..._typing import (
    Dtypes,
    ParsingMap,
    SeriesApply,
    SeriesPipe,
)
from ..._constants import (
    COL_DTYPE,
    COL_INDEX,
    INITIAL_DATE,
    REINDEX_NAME,
)

# Funciones base
_get_date_in_days: SeriesPipe = lambda s: s.dt.date - INITIAL_DATE
_get_days_difference: SeriesApply[timedelta] = lambda td: td.days
_get_seconds_in_day: SeriesPipe = lambda s: (s.dt.hour * 3600) + (s.dt.minute * 60) + (s.dt.second)
_get_day_fraction_from_seconds: SeriesPipe = lambda s: s / 86400
_get_seconds_in_timedelta: SeriesPipe = lambda s: (s.dt.days * 86400) + s.dt.seconds


_days_from_date: SeriesPipe = (
    lambda s: (
        s
        .pipe(_get_date_in_days)
        .apply(_get_days_difference)
    )
)
'Obtención de días transcurridos desde fecha.'
_day_fraction_from_datetime: SeriesPipe = (
    lambda s: (
        s
        .pipe(_get_seconds_in_day)
        .apply(_get_day_fraction_from_seconds)
    )
)
'Obtención de fracción de hora del día.'
_day_fraction_from_timedelta: SeriesPipe = (
    lambda s: (
        s
        .pipe(_get_seconds_in_timedelta)
        .pipe(_get_day_fraction_from_seconds)
    )
)
'Obtención de fracción de delta de tiempo.'

_parse_to: ParsingMap = {
    'datetime64[ns]': lambda s: _days_from_date(s) + _day_fraction_from_datetime(s),
    'datetime64[s]': lambda s: _days_from_date(s) + _day_fraction_from_datetime(s),
    'timedelta64[ns]': lambda s: _day_fraction_from_timedelta(s),
    'category': lambda s: s.astype('string'),
}
'Convertir a...'

def format_date_and_time_dtypes(data: pd.DataFrame) -> pd.DataFrame:
    """
    ### Formateo de fecha y tiempo
    Esta función formatea los tipos de dato de fecha, tiempo y delta de tiempo en
    valores numéricos entendibles por el motor de Hojas de Cálculo de Google.
    """

    raw_dtypes: list[Dtypes] = (
        data
        .reset_index(name= COL_DTYPE)
        .assign(dtype= lambda df: df[COL_DTYPE].astype('string'))
        .to_dict('records')
    )

    dtypes = {item[COL_INDEX]: item[COL_DTYPE] for item in raw_dtypes}

    for ( col, dtype ) in dtypes.items():
        if dtype in _parse_to:
            data = data.assign(**{col: _parse_to[dtype](data[col])})

    return data

def reorder_index(data: pd.DataFrame) -> pd.DataFrame:
    """
    ### Reordenar índice
    Esta función se asegura el índice del DataFrame no tenga datos repetivos a
    partir de reemplazar el índice original por uno limpio y consecutivo.
    """

    return (
        data
        .pipe(
            lambda df: (
                df
                # Se añade un índice y se renombra el anterior
                .reset_index(names= REINDEX_NAME)
                # Se descarta el índice extraído
                [df.columns]
            )
        )
    )
