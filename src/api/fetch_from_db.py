# src/api/fetch_from_db.py

import sqlite3
import pandas as pd
from pathlib import Path
from fastapi import HTTPException, status

from src.configurations import config
from src.logging.log_setup import get_logger

logger = get_logger(__name__)
db_path = Path(config.DB_DIR)


# 1. CORREZIONE: Accetta 'int | None' per essere compatibile con le routes
def fetch_data_from_db(table_name: str, da_anno: int | None, a_anno: int | None) -> list:
    """
    Recupera i dati da una tabella specificata, con filtri opzionali per anno.
    """
    if not db_path.exists():
        logger.error(f"Database '{db_path}' non trovato. Eseguire prima l'importazione.")
        # 2. CORREZIONE: Usa status code standard e formatta correttamente il messaggio
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Database non trovato al percorso: {db_path}")

    if da_anno is not None and a_anno is not None and a_anno < da_anno:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="'a_anno' deve essere maggiore o uguale a 'da_anno'.")

    try:
        with sqlite3.connect(db_path) as conn:
            # 3. CORREZIONE: Usa le doppie virgolette per il nome della tabella
            query = f'SELECT * FROM "{table_name}"'
            conditions = []
            params = {}

            if da_anno is not None:
                # 4. CORREZIONE (Best Practice): Metti tra virgolette anche il nome della colonna
                conditions.append(f'"{config.colonna_anno}" >= :da_anno')
                params['da_anno'] = da_anno

            if a_anno is not None:
                conditions.append(f'"{config.colonna_anno}" <= :a_anno')
                params['a_anno'] = a_anno

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            logger.debug(f"Esecuzione query: {query} con parametri: {params}")

            df = pd.read_sql_query(query, conn, params=params)

            if df.empty:
                return []
            return df.to_dict(orient='records')

    except sqlite3.Error as e:
        logger.error(f"Errore database durante la lettura della tabella {table_name}: {e}", exc_info=True)
        # 5. CORREZIONE: Non esporre i dettagli dell'errore al client
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Errore interno del server durante la lettura della tabella '{table_name}'.")
    except Exception as e:
        logger.error(f"Errore generico durante la lettura della tabella {table_name}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Errore generico del server.")
