import sqlite3
import pandas as pd
from pathlib import Path
from src.configurations import config
from src.logging.log_setup import get_logger

logger = get_logger(__name__)


def calcola_produttivita_nazionale():
    try:
        db_path = Path(config.DB_DIR)

        with sqlite3.connect(db_path) as conn:
            logger.info(f"Connessione al database {db_path} stabilita")

            # Prende il nome della tabella di input dalla configurazione
            table_input_name = Path(config.tabella_produttivita_pesca)

            # Prepara la query SQL per selezionare i dati necessari
            query_input = f'SELECT "{config.colonna_anno}", "{config.colonna_produttivita}" FROM "{table_input_name}"'

            # Esegue la query e carica i dati in un DataFrame di pandas
            df = pd.read_sql_query(query_input, conn)

            # Raggruppa i dati per anno e calcola la media della variazione percentuale
            risultati_df = df.groupby(config.colonna_anno)[config.colonna_produttivita].sum().reset_index()

            # Rinomina la colonna della media per claresezza
            risultati_df = risultati_df.rename(
                columns={config.colonna_produttivita: config.colonna_totale_nazionale_produttivita})

            # Arrotonda i valori della media a due cifre decimali
            risultati_df[config.colonna_totale_nazionale_produttivita] = risultati_df[
                config.colonna_totale_nazionale_produttivita].round(2)

            # Prende il nome della tabella di output dalla configurazione
            table_output_name = config.tabella_totale_nazionale_produttivita_pesca

            # Salva il DataFrame con i risultati in una nuova tabella del database
            risultati_df.to_sql(table_output_name, conn, if_exists='replace', index=False)

            logger.info(f"Produttività totale Nazionale calcolata e salvata in '{table_output_name}'")

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
