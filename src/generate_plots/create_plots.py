from typing import Optional
import pandas as pd
import plotly.express as px

from src.api.fetch_from_db import fetch_data_from_db
from src.configurations import config
from src.logging.log_setup import get_logger

logger = get_logger(__name__)


def crea_grafico_serie(
        table_name: str,
        y_col: str,
        title: str,
        color_col: Optional[str] = None,
        y_axis_title: Optional[str] = None
):
    """
        Crea e visualizza un grafico a linee per una serie storica.

        Args:
            table_name (str): Il nome della tabella da cui recuperare i dati.
            y_col (str): Il nome della colonna da usare per l'asse Y.
            title (str): Il titolo del grafico.
            color_col (str, optional): Il nome della colonna da usare per differenziare le linee (es. per macroarea).
            y_axis_title (str, optional): Il titolo per l'asse Y. Se non fornito, usa y_col.
    """
    logger.info(f"Inizio creazione del grafico per la tabella '{table_name}'")
    try:
        data = fetch_data_from_db(table_name, da_anno=None, a_anno=None)
        if not data:
            logger.warning(f"Nessun dato trovato per la tabella '{table_name}'")
            return
        df = pd.DataFrame(data)
        fig = px.line(
            df,
            x=config.colonna_anno,
            y=y_col,
            color=color_col,
            title=title,
            labels={
                config.colonna_anno: "Anno",
                y_col: y_axis_title or y_col
            },
            markers=True
        )
        fig.update_layout(
            xaxis_title="Anno",
            yaxis_title=y_axis_title or y_col,
            legend_title_text=config.colonna_macro_area if color_col else ""
        )
        logger.info(f"Visualizzazione grafico: {title}")
        fig.show()

    except Exception as e:
        logger.error(f"Errore durante la creazione del grafico per {table_name}: {e}", exc_info=True)
        logger.error(
            f"Controlla che i nomi delle colonne ({y_col, {color_col} }) siano corretti e presenti nella tabella '{table_name}'")
