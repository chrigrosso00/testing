import sqlite3
import pandas as pd
from pathlib import Path

# Importa le configurazioni e il logger personalizzato.
from src.configurations import config
from src.logging.log_setup import get_logger

# Inizializza il logger per questo modulo.
logger = get_logger(__name__)


def normalize_missing_data_by_interpolation():
    """
    Normalizza i dati mancanti nelle tabelle specificate tramite interpolazione lineare.
    Utilizza un approccio vettorizzato con pandas.transform per maggiore efficienza e leggibilità.
    Riempie SOLO i NaN esistenti all'interno degli anni già presenti per ciascuna regione.
    Le tabelle nel database vengono SOSTITUITE con i dati processati.
    """
    # Definisce il percorso del file di database.
    db_path = Path(config.DB_DIR)
    # Controlla se il database esiste, altrimenti registra un errore e termina.
    if not db_path.exists():
        logger.error(f"Database '{db_path}' non trovato. Eseguire prima l'importazione.")
        return

    # Dizionario che mappa le tabelle da processare con la colonna di valori corrispondente.
    tables_to_process = {
        config.tabella_andamento_occupazione_pesca: config.colonna_variazione_percentuale,
        config.tabella_importanza_economica_pesca: config.colonna_percentuale_valore_aggiunto,
        config.tabella_produttivita_pesca: config.colonna_produttivita,
    }

    # Inizializza i contatori per il riepilogo finale.
    tables_processed_successfully = 0
    total_nans_filled_overall = 0

    # Utilizza un blocco try...except per gestire errori a livello di connessione al database.
    try:
        # Apre una connessione al database. 'with' garantisce che la connessione venga chiusa automaticamente.
        with sqlite3.connect(db_path) as conn:
            logger.info(f"Connesso al database: '{db_path}' per il post-processing.")

            # Itera su ogni tabella e colonna specificata nel dizionario.
            for table_name, value_col in tables_to_process.items():
                logger.info(f"Inizio post-processing per la tabella: '{table_name}', colonna: '{value_col}'")

                try:
                    # Legge l'intera tabella dal database in un DataFrame di pandas.
                    original_df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)
                except pd.io.sql.DatabaseError as e:
                    # Se la tabella non può essere letta, registra un errore e passa alla successiva.
                    logger.error(f"Errore durante la lettura della tabella '{table_name}': {e}. Tabella saltata.")
                    continue

                # Se la tabella è vuota, non c'è nulla da processare.
                if original_df.empty:
                    logger.info(f"Tabella '{table_name}' è vuota. Saltata.")
                    continue

                # --- Preparazione Dati ---
                # Crea una copia del DataFrame per evitare di modificare l'originale durante il ciclo.
                df = original_df.copy()
                # Converte le colonne 'anno' e dei valori in formato numerico. 'coerce' trasforma i valori non validi in NaN.
                df[config.colonna_anno] = pd.to_numeric(df[config.colonna_anno], errors='coerce')
                df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
                # Rimuove le righe dove l'anno è NaN, poiché non possono essere usate per l'interpolazione.
                df.dropna(subset=[config.colonna_anno], inplace=True)
                # Converte la colonna 'anno' in tipo intero.
                df[config.colonna_anno] = df[config.colonna_anno].astype(int)

                # Ordina i dati per regione e poi per anno. Questo è fondamentale per un'interpolazione corretta.
                df.sort_values([config.colonna_regione, config.colonna_anno], inplace=True)

                # --- Logica di Interpolazione ---
                # Raggruppa i dati per regione e applica l'interpolazione a ogni gruppo.
                # 'transform' è efficiente perché applica la funzione a ogni gruppo e restituisce una Serie
                # con lo stesso indice del DataFrame originale, facilitando l'assegnazione.
                interpolated_series = df.groupby(config.colonna_regione)[value_col].transform(
                    # Usa una funzione lambda per applicare l'interpolazione lineare.
                    # L'interpolazione viene eseguita solo se ci sono almeno 2 punti dati validi per quella regione.
                    lambda s: s.interpolate(method='linear').round(2) if s.count() >= 2 else s
                )

                # --- Logging dei cambiamenti ---
                # Crea una maschera booleana per identificare dove un valore NaN è stato riempito.
                filled_mask = df[value_col].isna() & interpolated_series.notna()
                # Calcola il numero di valori riempiti in questa tabella.
                nans_filled_this_table = filled_mask.sum()

                # Se sono stati riempiti dei valori, logga i dettagli per ciascuno.
                if nans_filled_this_table > 0:
                    for index, row in df[filled_mask].iterrows():
                        new_value = interpolated_series.loc[index]
                        logger.info(
                            f"Tabella '{table_name}', Regione '{row[config.colonna_regione]}', "
                            f"Anno '{row[config.colonna_anno]}': Valore NaN interpolato a {new_value}."
                        )

                # Aggiorna la colonna nel DataFrame con i dati interpolati.
                df[value_col] = interpolated_series

                # --- Salvataggio nel Database ---
                try:
                    # Riordina le colonne per farle corrispondere all'ordine originale prima di salvare.
                    final_df = df.reindex(columns=original_df.columns)
                    # Salva il DataFrame aggiornato nel database, sostituendo la tabella esistente.
                    final_df.to_sql(table_name, conn, if_exists='replace', index=False)

                    # Logga un messaggio di successo basato sul fatto che siano stati riempiti o meno dei valori.
                    if nans_filled_this_table > 0:
                        logger.info(
                            f"Tabella '{table_name}' aggiornata. Totale valori NaN riempiti: {nans_filled_this_table}."
                        )
                    else:
                        logger.info(f"Tabella '{table_name}' processata. Nessun valore NaN da riempire.")

                    # Incrementa i contatori di successo.
                    tables_processed_successfully += 1
                    total_nans_filled_overall += nans_filled_this_table
                except Exception as e:
                    # Gestisce errori durante la scrittura nel database.
                    logger.error(f"Errore durante la scrittura dei dati per la tabella '{table_name}': {e}",
                                 exc_info=True)

            # Logga un riepilogo finale al termine di tutte le operazioni.
            logger.info(
                "Post-processing di interpolazione completato. "
                f"Tabelle processate con successo: {tables_processed_successfully}. "
                f"Totale NaN riempiti: {total_nans_filled_overall}."
            )

    except sqlite3.Error as e:
        # Gestisce errori specifici di SQLite.
        logger.error(f"Errore database SQLite durante il post-processing: {e}", exc_info=True)
    except Exception as e:
        # Gestisce qualsiasi altro errore generico.
        logger.error(f"Errore generico durante il post-processing: {e}", exc_info=True)


# Questo blocco viene eseguito solo se lo script è lanciato direttamente.
if __name__ == '__main__':
    logger.info("Avvio script di post-processing per normalizzazione dati (solo riempimento NaN)...")
    normalize_missing_data_by_interpolation()
    logger.info("Script di post-processing (solo riempimento NaN) terminato.")
