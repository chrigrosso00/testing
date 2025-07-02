from pathlib import Path
import sqlite3
import pandas as pd

from src.configurations import config
from src.logging.log_setup import get_logger

logger = get_logger(__name__)


def csv_to_sql():
    data_source_dir = Path(config.DATA_DIR)
    database_file_path = Path(config.DB_DIR)

    if not data_source_dir.is_dir():
        logger.error(f"La cartella dei dati '{data_source_dir}' non esiste:")
        return

    database_file_path.parent.mkdir(parents=True, exist_ok=True)
    conn = None
    try:
        conn = sqlite3.connect(database_file_path)
        logger.info(f"Connessione al database '{database_file_path}' stabilita")

        csv_files = list(data_source_dir.glob("*.csv"))

        if not csv_files:
            logger.warning(f"Nessun file CSV trovato nella cartella '{data_source_dir}'")
            return

        logger.info(f"Trovati {len(csv_files)} file CSV nella cartella '{data_source_dir}")

        table_names = [
            config.tabella_andamento_occupazione_pesca,
            config.tabella_importanza_economica_pesca,
            config.tabella_produttivita_pesca
        ]
        for csv_file_path in csv_files:
            file_stem = csv_file_path.stem

            table_name = None

            if file_stem in table_names:
                table_name = file_stem
            else:
                logger.warning(
                    f"Il nome del file CSV '{csv_file_path.name}' (stem: '{file_stem}') non corrisponde a nessun nome di tabella definito in config.py. File saltato.")
                continue

            logger.info(f"Processando il file '{csv_file_path.name}' per la tabella '{table_name}' ...")

            try:
                df = pd.read_csv(csv_file_path, delimiter=";")
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                logger.info(f"Dati da {csv_file_path.name} importati con successo nella tabella {table_name}")
            except Exception as e:
                logger.error(f"Errore durante l'importazione del file {csv_file_path.name}: {e}", exc_info=True)

        logger.info(f"Processo di importazione completato")

    finally:
        if conn:
            conn.close()
