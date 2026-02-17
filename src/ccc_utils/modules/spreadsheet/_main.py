from typing import Optional
import gspread
from gspread import WorksheetNotFound
import pandas as pd
from google.oauth2.service_account import Credentials
from ..._settings import CONFIG
from ._utils import (
    format_date_and_time_dtypes,
    reorder_index,
)

_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def _authenticate() -> gspread.auth.Client:

    # Autentización
    credentials = Credentials.from_service_account_file(
        f'{CONFIG.SPREADSHEET.GOOGLE_CLOUD_JSON_CREDENTIALS}.json',
        scopes= _SCOPES,
    )

    # Creación de una instancia de cliente
    client = gspread.authorize(credentials)

    return client

def _get_spreadsheet(
    spreadsheet_name: str,
    sheet_name: Optional[str],
) -> gspread.spreadsheet.Worksheet:

    # Creación de una instancia de cliente
    client = _authenticate()
    # Obtención del libro
    spreadsheets_file = client.open(spreadsheet_name)

    # Si un nombre de hoja fue proporcionado...
    if sheet_name:
        # Se abre ésta
        sheet = spreadsheets_file.worksheet(sheet_name)
    # Si no fue especificada una hoja...
    else:
        # Se abre la primera hoja encontrada
        sheet = spreadsheets_file.sheet1

    return sheet

def _create_spreadsheet(
    spreadsheet_name: str,
    sheet_name: Optional[str],
    data: pd.DataFrame,
) -> gspread.spreadsheet.Worksheet:

    # Creación de una instancia de cliente
    client = _authenticate()
    # Obtención del libro
    spreadsheets_file = client.open(spreadsheet_name)
    # Creación de la nueva hoja
    sheet = spreadsheets_file.add_worksheet(sheet_name, *data.shape)

    return sheet

def write(
    data: pd.DataFrame,
    spreadsheet_name: str,
    sheet_name: Optional[str] = None,
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
    """

    # Se intenta abrir la hoja de cálculo
    try:
        # Obtención de la hoja de cálculo
        sheet = _get_spreadsheet(spreadsheet_name, sheet_name)
    # En caso de que la hoja no exista...
    except WorksheetNotFound:
        # Se crea la nueva hoja en el libro 
        sheet = _create_spreadsheet(spreadsheet_name, sheet_name, data)

    # Obtención de las columnas del DataFrame
    columns = [data.columns.to_list(),]

    # Obtención del contenido del DataFrame
    content = (
        list(
            data
            # Reordenamiento y arreglo de índice
            .pipe(reorder_index)
            # Reasignación de tipos de dato para fecha y hora/duración
            .pipe(format_date_and_time_dtypes)
            # Transposición del DataFrame
            .T
            # Conversión a diccionario
            .to_dict('list')
            # Obtención de los valores
            .values()
        )
    )

    # Escritura en la hoja de cálculo
    sheet.update(columns, 'A1')
    sheet.update(content, 'A2')

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
    sheet = _get_spreadsheet(spreadsheet_name, sheet_name)
    # Obtención de los datos de la hoja
    data = sheet.get_all_records()
    # Creación del DataFrame
    df = pd.DataFrame(data)

    return df
