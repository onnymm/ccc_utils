import pandas as pd
from ..._constants import REINDEX_NAME
from ._resources import ColumnsFormatter

def format_date_and_time_dtypes(data: pd.DataFrame) -> pd.DataFrame:
    """
    ### Formateo de fecha y tiempo
    Esta función formatea los tipos de dato de fecha, tiempo y delta de tiempo en
    valores numéricos entendibles por el motor de Hojas de Cálculo de Google.
    """

    # Creación de instancia de formateador
    formatter = ColumnsFormatter(data)
    # Obtención de los datos formateados
    formated_data = formatter.formated_dtypes()

    return formated_data

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
