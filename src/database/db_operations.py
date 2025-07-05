# - Path per la gestione dei percorsi dei file in modo indipendente dal sistema operativo.
from pathlib import Path
# - sqlite3 per interagire con il database SQLite.
import sqlite3
# - pandas per la manipolazione e l'analisi dei dati, in particolare per leggere i file CSV.
import pandas as pd

# Importa l'oggetto di configurazione per accedere a percorsi e nomi di tabella.
from src.configurations import config
# Importa la funzione per ottenere un'istanza del logger.
from src.logging.log_setup import get_logger

# Inizializza il logger per questo modulo, per registrare eventi e errori.
logger = get_logger(__name__)


# Definisce la funzione principale per importare i dati dai file CSV al database SQLite.
def csv_to_sql():
    # Ottiene il percorso della cartella contenente i file CSV dalla configurazione.
    data_source_dir = Path(config.DATA_DIR)
    # Ottiene il percorso del file del database dalla configurazione.
    database_file_path = Path(config.DB_DIR)

    # Controlla se la cartella dei dati di origine esiste.
    if not data_source_dir.is_dir():
        # Se non esiste, registra un errore e termina la funzione.
        logger.error(f"La cartella dei dati '{data_source_dir}' non esiste.")
        return

    # Assicura che la cartella genitore del file di database esista, creandola se necessario.
    database_file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Utilizza un context manager 'with' per la connessione al database.
        # Questo garantisce che la connessione venga chiusa automaticamente alla fine del blocco,
        # sia in caso di successo che di errore.
        with sqlite3.connect(database_file_path) as conn:
            logger.info(f"Connessione al database '{database_file_path}' stabilita.")

            csv_files = list(data_source_dir.glob("*.csv"))

            if not csv_files:
                logger.warning(f"Nessun file CSV trovato nella cartella '{data_source_dir}'.")
                return

            logger.info(f"Trovati {len(csv_files)} file CSV nella cartella '{data_source_dir}'.")

            table_names = [
                config.tabella_andamento_occupazione_pesca,
                config.tabella_importanza_economica_pesca,
                config.tabella_produttivita_pesca
            ]

            for csv_file_path in csv_files:
                file_stem = csv_file_path.stem

                if file_stem not in table_names:
                    logger.warning(
                        f"Il nome del file CSV '{csv_file_path.name}' (stem: '{file_stem}') non corrisponde a "
                        f"nessun nome di tabella definito in config.py. File saltato.")
                    continue

                table_name = file_stem
                logger.info(f"Processando il file '{csv_file_path.name}' per la tabella '{table_name}'...")

                try:
                    df = pd.read_csv(csv_file_path, delimiter=";")
                    # if_exists="replace" elimina e ricrea la tabella se esiste già.
                    # index=False evita di scrivere l'indice del DataFrame nel database.
                    df.to_sql(table_name, conn, if_exists="replace", index=False)
                    logger.info(f"Dati da '{csv_file_path.name}' importati con successo nella tabella '{table_name}'.")
                except Exception as e:
                    logger.error(f"Errore durante l'importazione del file '{csv_file_path.name}': {e}", exc_info=True)

            logger.info("Processo di importazione completato.")

    except sqlite3.Error as e:
        # Gestisce eventuali errori a livello di database (es. file corrotto, permessi mancanti).
        logger.error(f"Errore del database durante la connessione a '{database_file_path}': {e}", exc_info=True)
