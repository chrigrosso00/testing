import pandas as pd
import sqlite3
from pathlib import Path

from src.configurations import config
from src.logging.log_setup import get_logger

logger = get_logger(__name__)


def calcola_media_occupazione_macroaree():
    """
        Calcola la media della variazione percentuale dell'occupazione per le 5 Macro Aree
        leggendo dati già puliti dal database SQLite e salva i risultati nel database.
        """
    try:
        db_path = Path(config.DB_DIR)

        # Utilizzo del context manager 'with' per la connessione al database
        with sqlite3.connect(db_path) as conn:
            logger.info(f"Connessione al database '{db_path}' stabilita")

            # Prende il nome della tabella di input dalla configurazione
            table_input_name = Path(config.tabella_andamento_occupazione_pesca)

            # Prepara la query SQL per selezionare i dati necessari
            query_input = f'SELECT "{config.colonna_anno}", "{config.colonna_regione}", "{config.colonna_variazione_percentuale}" FROM "{table_input_name}"'

            # Esegue la query e carica i dati in un DataFrame di pandas
            df = pd.read_sql_query(query_input, conn)

            # Aggiunge la colonna 'Macro Area' mappando ogni regione al suo gruppo geografico
            df[config.colonna_macro_area] = df[config.colonna_regione].map(config.macro_aree)

            # Raggruppa i dati per anno e regione e calcola la media della variazione percentuale
            risultati_df = df.groupby([config.colonna_anno, config.colonna_macro_area])[
                config.colonna_variazione_percentuale].mean().reset_index()

            # Rinomina la colonna della media per chiarezza
            risultati_df = risultati_df.rename(columns={
                config.colonna_variazione_percentuale: config.colonna_media_macroarea_variazione_percentuale_occupazione})

            # Arrotonda i valori della media a due cifre decimali
            risultati_df[config.colonna_media_macroarea_variazione_percentuale_occupazione] = risultati_df[
                config.colonna_media_macroarea_variazione_percentuale_occupazione].round(2)

            # Prende il nome della tabella di output dalla configurazione
            table_output_name = config.tabella_medie_macroaree_occupazione_pesca

            # Salva il DataFrame con i risultati in una nuova tabella del database
            risultati_df.to_sql(table_output_name, conn, if_exists='replace', index=False)

            logger.info(
                f"Media variazione percentuale occupazione Macro-Aree calcolata e salvata in '{table_output_name}'")

    except sqlite3.Error as e:
        logger.error(f"Errore SQLite durante l'operazione sul database: {e}", exc_info=True)
    except KeyError as e:
        logger.error(f"Errore di configurazione: una chiave attesa non è stata trovata in config. Dettagli: {e}",
                     exc_info=True)
    except Exception as e:
        logger.error(
            f"Errore generico durante il calcolo della media variazione percentuale occupazione Macro-Aree: {e}",
            exc_info=True)
