from typing import Optional
import gspread
from gspread import WorksheetNotFound
import pandas as pd
from google.oauth2.service_account import Credentials
from ..._constants import SPREADSHEETS_SCOPE
from ..._resources import CellStartPoints
from ..._settings import CONFIG
from ._utils import (
    format_date_and_time_dtypes,
    reorder_index,
)

def _authenticate() -> gspread.auth.Client:

    # Autentización
    credentials = Credentials.from_service_account_file(
        f'{CONFIG.SPREADSHEET.GOOGLE_CLOUD_JSON_CREDENTIALS}.json',
        scopes= SPREADSHEETS_SCOPE,
    )

    # Creación de una instancia de cliente
    client = gspread.authorize(credentials)

    return client

def get_existing_spreadsheet(
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

def get_or_create_spreadsheet(
    spreadsheet_name: str,
    sheet_name: str | None,
    data: pd.DataFrame,
) -> gspread.spreadsheet.Worksheet:

    # Se intenta abrir la hoja de cálculo
    try:
        # Obtención de la hoja de cálculo
        sheet = get_existing_spreadsheet(spreadsheet_name, sheet_name)
    # En caso de que la hoja no exista...
    except WorksheetNotFound:
        # Se crea la nueva hoja en el libro 
        sheet = _create_spreadsheet(spreadsheet_name, sheet_name, data)

    return sheet

def update_with_replace(
    data: pd.DataFrame,
    sheet: gspread.spreadsheet.Worksheet,
    cell_start_points: CellStartPoints,
) -> None:

    # Obtención del contenido del DataFrame
    content = get_content(data)

    # Obtención de las columnas del DataFrame
    columns = [data.columns.to_list(),]
    # Obtención de posición para colocar las columnas de los datos
    ( columns_cell, data_cell ) = cell_start_points.get_positions()

    # Escritura de las columnas en la hoja de cálculo en la posición establecida
    sheet.update(columns, columns_cell)

    # Escritura del contenido en la hoja de cálculo en la posición establecida
    sheet.update(content, data_cell)

def update_with_append(
    data: pd.DataFrame,
    sheet: gspread.spreadsheet.Worksheet,
    cell_start_points: CellStartPoints,
) -> None:

    # Obtención del contenido del DataFrame
    content = get_content(data)

    # Obtención del recuento de filas en la hoja
    total_rows = sheet.row_count
    # Se reasigna la posición inicial de la fila para los nuevos datos
    cell_start_points.data_initial_position.row = total_rows + 1
    # Se añaden las filas necesarias a la hoja
    sheet.add_rows(len(content))
    # Obtención de posición para colocar el contenido
    data_cell = cell_start_points.data_initial_position.to_string()

    # Escritura del contenido en la hoja de cálculo en la posición establecida
    sheet.update(content, data_cell)

def get_content(
    data: pd.DataFrame,
) -> list[dict]:

    # Obtención del contenido del DataFrame
    content: list[dict] = (
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

    return content
