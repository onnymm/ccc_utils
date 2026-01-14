import dotenv
import os
dotenv.load_dotenv()

from ._variable_presets import _PRESETS
from ccc_utils._typing import _T, _VariableConfig

def _load_variable_or_default(var_config: _VariableConfig[_T]) -> _T:
    # Destructuración de los argumentos
    ( name, preset, cast ) = var_config
    # Obtención de la variable de entorno
    variable_value = os.environ.get(f'CCC_{name}')
    # Si no existe ningún valor especificado en las variables de entorno...
    if variable_value is None:
        # Se usa el valor por defecto
        variable_value = preset
    # Si la variable fue establecida...
    else:
        # Se forza el casteo para recibir el valor en el formato correcto
        variable_value = cast(variable_value)

    return variable_value

class CONFIG:
    class SPREADSHEET:
        GOOGLE_CLOUD_JSON_CREDENTIALS = _load_variable_or_default(_PRESETS.SPREADSHEET.GOOGLE_CLOUD_JSON_CREDENTIALS)
