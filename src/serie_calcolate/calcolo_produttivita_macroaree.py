import pandas as pd
import sqlite3
from pathlib import Path
from src.logging.log_setup import get_logger
from src.configurations import config

logger = get_logger(__name__)


def calcola_produttivita_macroaree():
    """
        Calcola la produttività totale in migliaia di euro per le 5 Macro Aree
        leggendo i dati dal database SQLite e salva i risultati nel database.
        """
    try:
        db_path = Path(config.DB_DIR)
        with sqlite3.connect(db_path) as conn:
            logger.info(f"Connessione al database {db_path} stabilita")

            # Prende il nome della tabella di input dalla configurazione
            table_input_name = Path(config.tabella_produttivita_pesca)

            # Prepara la query SQL per selezionare i dati necessari
            query_input = f'SELECT "{config.colonna_anno}", "{config.colonna_regione}", "{config.colonna_produttivita}" FROM "{table_input_name}"'

            # Esegue la query e carica i dati in un DataFrame di pandas
            df = pd.read_sql_query(query_input, conn)

            # Aggiunge la colonna 'Macro Area' mappando ogni regione al suo gruppo geografico
            df[config.colonna_macro_area] = df[config.colonna_regione].map(config.macro_aree)

            # Raggruppa i dati per anno e regione e calcola la media della variazione percentuale
            risultati_df = df.groupby([config.colonna_anno, config.colonna_macro_area])[
                config.colonna_produttivita].sum().reset_index()

            # Rinomina la colonna della media per claresezza
            risultati_df = risultati_df.rename(
                columns={config.colonna_produttivita: config.colonna_totale_macroarea_produttivita})

            # Arrotonda i valori della media a due cifre decimali
            risultati_df[config.colonna_totale_macroarea_produttivita] = risultati_df[
                config.colonna_totale_macroarea_produttivita].round(2)

            # Prende il nome della tabella di output dalla configurazione
            table_output_name = config.tabella_totali_macroaree_produttivita_pesca

            # Salva il DataFrame con i risultati in una nuova tabella del database
            risultati_df.to_sql(table_output_name, conn, if_exists='replace', index=False)

            logger.info(f"Produttività totale Macro-Aree calcolata e salvata in '{table_output_name}'")

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
