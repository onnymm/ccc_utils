import re
from typing import Optional

_COLUMN_FORMAT = r'[A-Z]+'
_ROW_FORMAT = r'\d+'

class _CellPoint:
    column: str
    row: int

    def __init__(
        self,
        address: str,
    ) -> None:

        # Obtención de posición de columna y fila
        self.column = self._get_column_position(address)
        self.row = self._get_row_position(address)

    def copy(
        self,
    ) -> _CellPoint:

        # Creación de nueva instancia
        new = _CellPoint(f'{self}')

        return new

    def __repr__(
        self,
    ) -> str:

        # Obtención de valores
        column = self.column
        row = self.row

        # Creación de representación
        repr_ = f'{column}{row}'

        return repr_

    def _get_column_position(
        self,
        address: str,
    ) -> str:

        # Búsqueda de la posición de columna
        [ position ] = re.findall(_COLUMN_FORMAT, address)

        return position

    def _get_row_position(
        self,
        address: str,
    ) -> str:

        # Búsqueda de la posición de fila
        [ position ] = re.findall(_ROW_FORMAT, address)
        # Conversión del valor de posición a entero
        position = int(position)

        return position

class CellStartPoints:
    _DEFAULT_CELL = 'A1'

    def __init__(
        self,
        columns_initial_position: str = _DEFAULT_CELL,
        data_initial_position: Optional[str] = None,
    ) -> None:

        # Obtención de referencia de celda de columnas
        cols_cell_position = self._set_cell_position(columns_initial_position)

        # Si no se proporcionó una referecia de desfase para los datos...
        if data_initial_position is None:
            # Se copia la referencia desde la posición de columnas
            data_cell_position = cols_cell_position.copy()
            # Se incrementa una unidad a las filas
            data_cell_position.row += 1

        # Si se proporcionó una referencia de desfase para los datos...
        else:
            data_cell_position = self._set_cell_position(data_initial_position)

        # Asignación de valores
        self.columns_initial_position = cols_cell_position
        self.data_initial_position = data_cell_position

    def get_positions(
        self,
    ) -> tuple[str, str]:

        columns_initial_position = str(self.columns_initial_position)
        data_initial_position = str(self.data_initial_position)

        return (columns_initial_position, data_initial_position)

    def _set_cell_position(self, columns_cell: str) -> _CellPoint:

        # Inicialización de instancia de punto de celda
        columns_position = _CellPoint(columns_cell)

        return columns_position
