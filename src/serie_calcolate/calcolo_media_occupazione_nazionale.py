import pandas as pd
import sqlite3
from pathlib import Path

from src.configurations import config
from src.logging.log_setup import get_logger

logger = get_logger(__name__)


def calcola_media_occupazione_nazionale():
    """
        Calcola la media della variazione percentuale dell'occupazione a livello Nazionale
        leggendo i dati dal database SQLite e salva i risultati nel database.
        """
    try:
        # Ottiene il percorso del database dal file di configurazione
        db_path = Path(config.DB_DIR)

        # Usa un context manager per connettersi al DB (garantisce la chiusura automatica)
        with sqlite3.connect(db_path) as conn:
            logger.info(f"Connessione al database '{db_path}' stabilita")

            # Prende il nome della tabella di input dalla configurazione
            table_input_name = config.tabella_andamento_occupazione_pesca

            # Prepara la query SQL per selezionare i dati necessari
            query_input = f'SELECT "{config.colonna_anno}", "{config.colonna_variazione_percentuale}" FROM "{table_input_name}"'

            # Esegue la query e carica i dati in un DataFrame di pandas
            df = pd.read_sql_query(query_input, conn)

            # Raggruppa i dati per anno e calcola la media della variazione percentuale
            risultati_df = df.groupby(config.colonna_anno)[config.colonna_variazione_percentuale].mean().reset_index()

            # Rinomina la colonna della media per chiarezza
            risultati_df = risultati_df.rename(columns={
                config.colonna_variazione_percentuale: config.colonna_media_nazionale_variazione_percentuale_occupazione})

            # Arrotonda i valori della media a due cifre decimali
            risultati_df[config.colonna_media_nazionale_variazione_percentuale_occupazione] = risultati_df[
                config.colonna_media_nazionale_variazione_percentuale_occupazione].round(2)

            # Prende il nome della tabella di output dalla configurazione
            table_output_name = config.tabella_media_nazionale_occupazione_pesca

            # Salva il DataFrame con i risultati in una nuova tabella del database
            risultati_df.to_sql(table_output_name, conn, if_exists='replace', index=False)

            logger.info(
                f"Media variazione percentuale occupazione Nazionale calcolata e salvata in '{table_output_name}'")

    # Gestisce specifici errori del database
    except sqlite3.Error as e:
        logger.error(f"Errore SQLite durante l'operazione sul database: {e}", exc_info=True)
    # Gestisce errori dovuti a nomi di colonne/tabelle mancanti nella configurazione
    except KeyError as e:
        logger.error(f"Errore di configurazione: una chiave attesa non è stata trovata in config. Dettagli: {e}",
                     exc_info=True)
    # Gestisce qualsiasi altro errore imprevisto
    except Exception as e:
        logger.error(
            f"Errore generico durante il calcolo della media nazionale dell'occupazione: {e}",
            exc_info=True)
