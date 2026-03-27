from typing import Optional
import pandas as pd
from ..._constants import COLUMNS_INITIAL_POSITION
from ..._resources import CellStartPoints
from ..._typing import WriteMethodOption
from ...errors import InvalidWriteMethod
from ._core import (
    get_existing_spreadsheet,
    get_or_create_spreadsheet,
    update_with_append,
    update_with_replace,
)

def write(
    data: pd.DataFrame,
    spreadsheet_name: str,
    sheet_name: Optional[str] = None,
    columns_start_position: Optional[str] = COLUMNS_INITIAL_POSITION,
    data_start_position: Optional[str] = None,
    method: WriteMethodOption = 'replace',
) -> None:
    """
    ### Guardar en Hojas de Cálculo
    Esta función escribe los datos del Pandas DataFrame provisto en una hoja
    de hoja de cálculo especificada.

    Si el nombre de la hoja proporcionado apunta a una hoja que no existe, ésta
    se creará.

    :param DataFrame data: Datos a escribir en el archivo de hojas de
        cálculo.
    :param str spreadsheet_name: Nombre del archivo de Hojas de Cálculo.
    :param str sheet_name: Nombre de la hoja del archivo de Hojas de Cálculo.
    :param str columns_start_position: Posición inicial para comenzar a colocar las
    columnas.
    :param str data_start_position: Posición inicial para comenzar a colocar los
    datos sin incluir las columnas.
    :param WriteMethodOption method: Método de escritura.
    """

    # Obtención o creación de la hoja
    sheet = get_or_create_spreadsheet(spreadsheet_name, sheet_name, data)
    # Inicialización de instancia de puntos de inicio de celdas
    cell_start_points = CellStartPoints(columns_start_position, data_start_position)

    # Si el tipo de método es de reemplazo...
    if method == 'replace':
        # Se realiza la escritura de datos con reemplazo
        update_with_replace(data, sheet, cell_start_points)

    # Si el tipo de método es de añadir datos al final...
    elif method == 'append':
        # Se realiza la escritura de datos añadiéndolos al final
        update_with_append(data, sheet, cell_start_points)

    else:
        # Se lanza error de método de escritura inválido
        raise InvalidWriteMethod(f'El método "{method}" no es válido.')

def load(
    spreadsheet_name: str,
    sheet_name: Optional[str] = None,
) -> pd.DataFrame:
    """
    ### Cargar desde Hojas de Cálculo
    Esta función carga un DataFrame a partir de los datos en una hoja de un
    archivo de Hojas de Cálculo.

    :param str spreadsheet_name: Nombre del archivo de Hojas de Cálculo.
    :param str sheet_name: Nombre de la hoja del archivo de Hojas de Cálculo.
    """

    # Obtención de la hoja de cálculo
    sheet = get_existing_spreadsheet(spreadsheet_name, sheet_name)
    # Obtención de los datos de la hoja
    data = sheet.get_all_records()
    # Creación del DataFrame
    df = pd.DataFrame(data)

    return df
