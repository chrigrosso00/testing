import sqlite3
import pandas as pd
from pathlib import Path
from fastapi import HTTPException, status

from src.configurations import config
from src.logging.log_setup import get_logger

# Inizializza il logger per questo modulo, per registrare eventi e errori.
logger = get_logger(__name__)
# Definisce il percorso del database SQLite utilizzando il percorso specificato nella configurazione.
db_path = Path(config.DB_DIR)


def fetch_data_from_db(table_name: str, da_anno: int | None, a_anno: int | None) -> list:
    """
    Recupera i dati da una tabella specificata, con filtri opzionali per anno.
    """
    # Controlla se il file del database esiste effettivamente nel percorso specificato.
    if not db_path.exists():
        # Se il database non viene trovato, registra un errore e solleva un'eccezione HTTP 404 (Not Found).
        logger.error(f"Database '{db_path}' non trovato. Eseguire prima l'importazione.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Database non trovato al percorso: {db_path}")

    # Valida che, se entrambi gli anni sono forniti, l'anno di fine non sia precedente all'anno di inizio.
    if da_anno is not None and a_anno is not None and a_anno < da_anno:
        # Se la validazione fallisce, solleva un'eccezione HTTP 400 (Bad Request).
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="'a_anno' deve essere maggiore o uguale a 'da_anno'.")

    try:
        # Apre una connessione al database. L'uso di 'with' garantisce che la connessione venga chiusa automaticamente.
        with sqlite3.connect(db_path) as conn:
            # Costruisce la parte iniziale della query SQL per selezionare tutti i record.
            query = f'SELECT * FROM "{table_name}"'
            conditions = []  # Lista per memorizzare le condizioni del filtro (clausola WHERE).
            params = {}  # Dizionario per i parametri della query, per prevenire attacchi di SQL injection.

            # Se è stato fornito un anno di inizio, aggiunge la relativa condizione.
            if da_anno is not None:
                conditions.append(f'"{config.colonna_anno}" >= :da_anno')
                params['da_anno'] = da_anno

            # Se è stato fornito un anno di fine, aggiunge la relativa condizione.
            if a_anno is not None:
                conditions.append(f'"{config.colonna_anno}" <= :a_anno')
                params['a_anno'] = a_anno

            # Se ci sono condizioni di filtro, le aggiunge alla query principale, unite da "AND".
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            # Registra la query completa e i parametri per scopi di debug.
            logger.debug(f"Esecuzione query: {query} con parametri: {params}")

            # Esegue la query utilizzando pandas, che popola un DataFrame con i risultati.
            # 'params' viene passato per una sostituzione sicura dei valori nella query.
            df = pd.read_sql_query(query, conn, params=params)

            # Se il DataFrame è vuoto (nessun risultato trovato), restituisce una lista vuota.
            if df.empty:
                return []

            # Altrimenti, converte il DataFrame in una lista di dizionari e la restituisce.
            return df.to_dict(orient='records')

    # Gestisce specificamente gli errori che possono verificarsi durante le operazioni con il database SQLite.
    except sqlite3.Error as e:
        logger.error(f"Errore database durante la lettura della tabella {table_name}: {e}", exc_info=True)
        # Solleva un'eccezione HTTP 500 (Internal Server Error) con un messaggio generico per sicurezza.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Errore interno del server durante la lettura della tabella '{table_name}'.")
    # Gestisce qualsiasi altra eccezione generica non prevista.
    except Exception as e:
        logger.error(f"Errore generico durante la lettura della tabella {table_name}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Errore generico del server.")
