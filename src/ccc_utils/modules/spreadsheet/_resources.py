from dataclasses import dataclass
from datetime import timedelta
from typing import Callable
import pandas as pd
import numpy as np
from pandas._typing import AstypeArg
from ..._constants import (
    COLUMN,
    INITIAL_DATE,
    SECONDS_IN_ONE,
)
from ..._typing import (
    ColumnAssignation,
    Dtypes,
    ParsingMap,
    SeriesApply,
    SeriesFromDataFrame,
    SeriesPipe,
)

_seconds_to_numeric: SeriesPipe = lambda s: s / SECONDS_IN_ONE.DAY
'Segundos a decimal.'

# Funciones para [datetime]
_date_to_days: SeriesPipe = lambda s: s.dt.date - INITIAL_DATE
'Fecha a días en codificación de fecha en Excel.'
_days_delta: SeriesApply[timedelta] = lambda td: td.days if td is not np.nan else np.nan
'Delta de días desde fecha inicial en codificación de fecha en Excel.'

_hours_to_seconds: SeriesPipe = lambda s: s.dt.hour * SECONDS_IN_ONE.HOUR
'Horas a segundos.'
_minutes_to_seconds: SeriesPipe = lambda s: s.dt.minute * SECONDS_IN_ONE.MINUTE
'Minutos a segundos.'

_partial_day_to_seconds: SeriesPipe = lambda s: _hours_to_seconds(s) + _minutes_to_seconds(s) + s.dt.second
'Día parcial a segundos.'

# Funciones para [timedelta]
_days_to_seconds: SeriesPipe = lambda s: s.dt.days * SECONDS_IN_ONE.DAY
'Días a segundos.'
_timdelta_to_seconds: SeriesPipe = lambda s: _days_to_seconds(s) + s.dt.seconds
'Delta de tiempo a segundos.'
_replace_nat_with_none: SeriesPipe = (
    lambda s: (
        s
        .astype('float64')
        .astype('object')
        .replace({np.nan: None})
    )
)
'Función para conversión de dtype y reemplazo de valores `NaT` por `None`.'

_date_to_integer: SeriesPipe = (
    lambda s: (
        s
        .pipe(_date_to_days)
        .apply(_days_delta)
    )
)
'Obtención de días transcurridos desde fecha.'

_day_fraction_from_datetime: SeriesPipe = (
    lambda s: (
        s
        .pipe(_partial_day_to_seconds)
        .apply(_seconds_to_numeric)
    )
)
'Obtención de fracción de hora del día.'

_datetime_to_numeric_fn: SeriesPipe = (
    lambda s: (
        (
            _date_to_integer(s)
            + _day_fraction_from_datetime(s)
        )
        .pipe(_replace_nat_with_none)
    )
)
'Formateo de tipo `datetime` a codificación numérica de Excel.'

_timedelta_to_numeric_fn: SeriesPipe = (
    lambda s: (
        s
        .pipe(_timdelta_to_seconds)
        .pipe(_seconds_to_numeric)
        .pipe(_replace_nat_with_none)
    )
)
'Formateo de tipo `timedelta` a codificación numérica de Excel.'

_generic_to_string_fn: SeriesPipe = lambda s: s.astype('string')
'Formateo de tipo genérico a texto.'

_parse_to: ParsingMap = {
    'datetime64[as]': _datetime_to_numeric_fn,
    'datetime64[D]': _datetime_to_numeric_fn,
    'datetime64[fs]': _datetime_to_numeric_fn,
    'datetime64[h]': _datetime_to_numeric_fn,
    'datetime64[M]': _datetime_to_numeric_fn,
    'datetime64[m]': _datetime_to_numeric_fn,
    'datetime64[ms]': _datetime_to_numeric_fn,
    'datetime64[ns]': _datetime_to_numeric_fn,
    'datetime64[ps]': _datetime_to_numeric_fn,
    'datetime64[s]': _datetime_to_numeric_fn,
    'datetime64[us]': _datetime_to_numeric_fn,
    'datetime64[W]': _datetime_to_numeric_fn,
    'datetime64[Y]': _datetime_to_numeric_fn,
    'datetime64[μs]': _datetime_to_numeric_fn,
    'timedelta64[as]': _timedelta_to_numeric_fn,
    'timedelta64[D]': _timedelta_to_numeric_fn,
    'timedelta64[fs]': _timedelta_to_numeric_fn,
    'timedelta64[h]': _timedelta_to_numeric_fn,
    'timedelta64[M]': _timedelta_to_numeric_fn,
    'timedelta64[m]': _timedelta_to_numeric_fn,
    'timedelta64[ms]': _timedelta_to_numeric_fn,
    'timedelta64[ns]': _timedelta_to_numeric_fn,
    'timedelta64[ps]': _timedelta_to_numeric_fn,
    'timedelta64[s]': _timedelta_to_numeric_fn,
    'timedelta64[us]': _timedelta_to_numeric_fn,
    'timedelta64[W]': _timedelta_to_numeric_fn,
    'timedelta64[Y]': _timedelta_to_numeric_fn,
    'timedelta64[μs]': _timedelta_to_numeric_fn,
    'category': _generic_to_string_fn,
    'str': _generic_to_string_fn,
    'string': _generic_to_string_fn,
    'string[pyarrow]': _generic_to_string_fn,
    'string[python]': _generic_to_string_fn,
    'object': _generic_to_string_fn,
    'O': _generic_to_string_fn,
}
'Convertir a...'

@dataclass(slots= True)
class _ColumnToTransform:
    index: str
    dtype: AstypeArg

    def __repr__(
        self,
    ) -> str:

        # Obtención de atributos
        class_name = self.__class__.__name__
        index = self.index
        dtype = self.dtype

        # Construcción de representación en cadena de texto
        repr_ = f'{class_name}(index={index}, dtype={dtype})'

        return repr_

class ColumnsFormatter:
    _columns_to_transform: list[_ColumnToTransform]

    def __init__(
        self,
        data: pd.DataFrame,
    ) -> None:
        
        # Se guarda el DataFrame provisto
        self._data = data.copy()
        # Obtención de tipos de dato por columna
        dtypes_per_column = self._get_dtypes_per_column(data)
        # Creación de instancias de columnas a transformar
        self._columns_to_transform = [_ColumnToTransform(**item) for item in dtypes_per_column]

    def formated_dtypes(
        self,
    ) -> pd.DataFrame:

        return (
            self._data
            .pipe(self._to_spreadsheet_dtypes)
        )

    def _to_spreadsheet_dtypes(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:

        # Inicialización de diccionario de columnas a reasignar de tipo de dato
        to_assign: dict[str, Callable[[pd.DataFrame], pd.Series]] = {}

        # Iteración por cada columna a transformar
        for column in self._columns_to_transform:
            # Si el tipo de dato está en los tipos de dato a convertir...
            if column.dtype in _parse_to:
                # Obtención del nombre y del tipo de dato
                column_name = column.index
                column_dtype = column.dtype

                # Obtención de la función de parseo
                to_assign[column_name] = self._build_parse_callback(
                    column_name,
                    column_dtype,
                )

        # Si hay columnas cuyo tipo de dato hay que reasignar...
        if to_assign:

            return (
                data
                # Reasignación de tipos de dato
                .assign(**to_assign)
            )

        # Si no hay columnas cuyo tipo de dato hay que reasignar...
        else:

            return data

    def _get_dtypes_per_column(
        self,
        data: pd.DataFrame,
    ) -> list[Dtypes]:

        # Función para formatear referencia de tipo de dato en su representación en string
        dtype_repr_fn: ColumnAssignation = {
            COLUMN.DTYPE: (
                lambda df: (
                    df
                    [COLUMN.DTYPE]
                    .astype('string')
                )
            )
        }

        # Obtención de tipos de dato por columna
        dtypes_per_column: list[Dtypes] = (
            data
            # Obtención de tipos de dato
            .dtypes
            # Reseteo de índice
            .reset_index(name= COLUMN.DTYPE)
            # Obtención del nombre del tipo de dato en texto
            .assign(**dtype_repr_fn)
            # Conversión a lista de diccionarios
            .to_dict('records')
        )

        return dtypes_per_column

    def _build_parse_callback(
        self,
        column_name: str,
        column_dtype: AstypeArg
    ) -> SeriesFromDataFrame:

        def parser(df: pd.DataFrame) -> pd.Series:
            dtype_parse_fn = _parse_to[column_dtype]
            return (
                df[column_name]
                .pipe(dtype_parse_fn)
            )

        return parser

def format_date_and_time_dtypesv2(data: pd.DataFrame) -> pd.DataFrame:
    """
    ### Formateo de fecha y tiempo
    Esta función formatea los tipos de dato de fecha, tiempo y delta de tiempo en
    valores numéricos entendibles por el motor de Hojas de Cálculo de Google.
    """

    # Función para formatear referencia de tipo de dato en su representación en string
    dtype_repr_fn: ColumnAssignation = {
        COLUMN.DTYPE: (
            lambda df: (
                df
                [COLUMN.DTYPE]
                .astype('string')
            )
        )
    }

    # Obtención de tipos de dato por columna
    dtypes_per_column: list[Dtypes] = (
        data
        # Obtención de tipos de dato
        .dtypes
        # Reseteo de índice
        .reset_index(name= COLUMN.DTYPE)
        # Obtención del nombre del tipo de dato en texto
        .assign(**dtype_repr_fn)
        # Conversión a lista de diccionarios
        .to_dict('records')
    )

    # Creación de instancias de columnas a transformar
    columns_to_transform = [_ColumnToTransform(**item) for item in dtypes_per_column]
    # Creación de instancia de formateador
    formatter = ColumnsFormatter(columns_to_transform)

    return (
        data
        .pipe(formatter._to_spreadsheet_dtypes)
    )