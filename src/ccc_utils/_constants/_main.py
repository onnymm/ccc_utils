from datetime import date

PROJECT_PREFIX = 'CCC_'
'`Literal[str]` Prefijo de projecto para variables de entorno.'

INITIAL_DATE = date(1899, 12, 30)
"""
### Fecha inicial de Excel
Valor de fecha usado como día `0` para codificar valores de fecha y fecha/hora
en Excel.
"""

COLUMNS_INITIAL_POSITION = 'A1'
'Posición inicial en hoja para comenzar a insertar datos.'

class SECONDS_IN_ONE:
    """
    `CONST` Cantidad de segundos en un...
    """
    MINUTE = 60
    'Cantidad de segundos que hay en 1 minuto.'
    HOUR = 3600
    'Cantidad de segundos que hay en 1 hora.'
    DAY = 86400
    'Cantidad de segundos que hay en 1 día.'

class COLUMN:
    """
    `CONST` Nombres de columna en atributo `dtypes` de DataFrames.
    """
    DTYPE = 'dtype'
    INDEX = 'index'

REINDEX_NAME = '__index__'
"""
`Literal[str]` Nombre predeterminado para renombrar índices en método
`reset_index` de DataFrames.
"""

class _SCOPE_AUTH:
    SPREADSHEETS = "https://www.googleapis.com/auth/spreadsheets"
    DRIVE = "https://www.googleapis.com/auth/drive"

SPREADSHEETS_SCOPE = [
    _SCOPE_AUTH.SPREADSHEETS,
    _SCOPE_AUTH.DRIVE,
]
