import sqlite3
import pandas as pd
from pathlib import Path

from src.configurations import config
from src.logging.log_setup import get_logger

logger = get_logger(__name__)


def normalize_missing_data_by_interpolation():
    """
    Normalizza i dati mancanti nelle tabelle specificate tramite interpolazione lineare.
    Utilizza un approccio vettorizzato con pandas.transform per maggiore efficienza e leggibilità.
    Riempie SOLO i NaN esistenti all'interno degli anni già presenti per ciascuna regione.
    Le tabelle nel database vengono SOSTITUITE con i dati processati.
    """
    db_path = Path(config.DB_DIR)
    if not db_path.exists():
        logger.error(f"Database '{db_path}' non trovato. Eseguire prima l'importazione.")
        return

    tables_to_process = {
        config.tabella_andamento_occupazione_pesca: config.colonna_variazione_percentuale,
        config.tabella_importanza_economica_pesca: config.colonna_percentuale_valore_aggiunto,
        config.tabella_produttivita_pesca: config.colonna_produttivita,
    }

    tables_processed_successfully = 0
    total_nans_filled_overall = 0

    # --- REFACTOR 1: Utilizzo del context manager 'with' per la connessione ---
    # Questo garantisce che la connessione sia chiusa automaticamente alla fine del blocco.
    try:
        with sqlite3.connect(db_path) as conn:
            logger.info(f"Connesso al database: '{db_path}' per il post-processing.")

            for table_name, value_col in tables_to_process.items():
                logger.info(f"Inizio post-processing per la tabella: '{table_name}', colonna: '{value_col}'")

                try:
                    original_df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)
                except pd.io.sql.DatabaseError as e:
                    logger.error(f"Errore durante la lettura della tabella '{table_name}': {e}. Tabella saltata.")
                    continue

                if original_df.empty:
                    logger.info(f"Tabella '{table_name}' è vuota. Saltata.")
                    continue

                # --- Preparazione Dati ---
                df = original_df.copy()
                df[config.colonna_anno] = pd.to_numeric(df[config.colonna_anno], errors='coerce')
                df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
                df.dropna(subset=[config.colonna_anno], inplace=True)
                df[config.colonna_anno] = df[config.colonna_anno].astype(int)

                # Ordinamento per regione e anno, cruciale per l'interpolazione corretta per gruppo
                df.sort_values([config.colonna_regione, config.colonna_anno], inplace=True)

                # --- REFACTOR 2: Logica di Interpolazione semplificata con transform ---
                # 'transform' applica una funzione a ciascun gruppo (regione) e restituisce una Serie
                # con lo stesso indice del DataFrame di partenza, eliminando il bisogno di un loop esplicito.
                interpolated_series = df.groupby(config.colonna_regione)[value_col].transform(
                    lambda s: s.interpolate(method='linear').round(2) if s.count() >= 2 else s
                )

                # --- Logging dei cambiamenti ---
                # Identifica dove un NaN è stato riempito confrontando la serie originale con quella interpolata
                filled_mask = df[value_col].isna() & interpolated_series.notna()
                nans_filled_this_table = filled_mask.sum()

                if nans_filled_this_table > 0:
                    # Logga i dettagli per ogni valore riempito
                    for index, row in df[filled_mask].iterrows():
                        new_value = interpolated_series.loc[index]
                        logger.info(
                            f"Tabella '{table_name}', Regione '{row[config.colonna_regione]}', "
                            f"Anno '{row[config.colonna_anno]}': Valore NaN interpolato a {new_value}."
                        )

                # Aggiorna la colonna nel DataFrame con i dati interpolati
                df[value_col] = interpolated_series

                # --- Salvataggio nel Database ---
                try:
                    # Assicura che l'ordine delle colonne corrisponda all'originale prima di salvare
                    final_df = df.reindex(columns=original_df.columns)
                    final_df.to_sql(table_name, conn, if_exists='replace', index=False)

                    if nans_filled_this_table > 0:
                        logger.info(
                            f"Tabella '{table_name}' aggiornata. Totale valori NaN riempiti: {nans_filled_this_table}."
                        )
                    else:
                        logger.info(f"Tabella '{table_name}' processata. Nessun valore NaN da riempire.")

                    tables_processed_successfully += 1
                    total_nans_filled_overall += nans_filled_this_table
                except Exception as e:
                    logger.error(f"Errore durante la scrittura dei dati per la tabella '{table_name}': {e}",
                                 exc_info=True)

            logger.info(
                "Post-processing di interpolazione completato. "
                f"Tabelle processate con successo: {tables_processed_successfully}. "
                f"Totale NaN riempiti: {total_nans_filled_overall}."
            )

    except sqlite3.Error as e:
        logger.error(f"Errore database SQLite durante il post-processing: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Errore generico durante il post-processing: {e}", exc_info=True)
    # Il 'finally' per chiudere la connessione non è più necessario grazie a 'with'


if __name__ == '__main__':
    logger.info("Avvio script di post-processing per normalizzazione dati (solo riempimento NaN)...")
    normalize_missing_data_by_interpolation()
    logger.info("Script di post-processing (solo riempimento NaN) terminato.")
