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
        logger.error(f"La cartella dei dati '{data_source_dir}' non esiste:")
        return

    # Assicura che la cartella genitore del file di database esista, creandola se necessario.
    database_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Inizializza la variabile di connessione a None.
    conn = None
    # Usa un blocco try...finally per garantire che la connessione al database venga sempre chiusa.
    try:
        # Stabilisce una connessione con il file di database SQLite.
        conn = sqlite3.connect(database_file_path)
        logger.info(f"Connessione al database '{database_file_path}' stabilita")

        # Cerca tutti i file con estensione .csv nella cartella dei dati.
        csv_files = list(data_source_dir.glob("*.csv"))

        # Se non vengono trovati file CSV, registra un avviso e termina la funzione.
        if not csv_files:
            logger.warning(f"Nessun file CSV trovato nella cartella '{data_source_dir}'")
            return

        # Registra il numero di file CSV trovati.
        logger.info(f"Trovati {len(csv_files)} file CSV nella cartella '{data_source_dir}")

        # Definisce una lista di nomi di tabella validi presi dalla configurazione.
        # Questi sono i nomi che ci aspettiamo di trovare come nomi di file (senza estensione).
        table_names = [
            config.tabella_andamento_occupazione_pesca,
            config.tabella_importanza_economica_pesca,
            config.tabella_produttivita_pesca
        ]

        # Itera su ogni file CSV trovato.
        for csv_file_path in csv_files:
            # Estrae il nome del file senza l'estensione (es. "file.csv" -> "file").
            file_stem = csv_file_path.stem

            # Inizializza il nome della tabella a None.
            table_name = None

            # Controlla se il nome del file (senza estensione) corrisponde a uno dei nomi di tabella validi.
            if file_stem in table_names:
                # Se c'è una corrispondenza, assegna il nome alla variabile table_name.
                table_name = file_stem
            else:
                # Altrimenti, registra un avviso e salta al prossimo file nel ciclo.
                logger.warning(
                    f"Il nome del file CSV '{csv_file_path.name}' (stem: '{file_stem}') non corrisponde a nessun nome di tabella definito in config.py. File saltato.")
                continue

            # Registra quale file si sta processando e in quale tabella verrà inserito.
            logger.info(f"Processando il file '{csv_file_path.name}' per la tabella '{table_name}' ...")

            # Blocco try...except per gestire errori specifici durante la lettura e l'importazione del singolo file.
            try:
                # Legge il file CSV in un DataFrame di pandas, specificando che il delimitatore è il punto e virgola.
                df = pd.read_csv(csv_file_path, delimiter=";")
                # Scrive il contenuto del DataFrame nella tabella SQL corrispondente.
                # if_exists="replace" significa che se la tabella esiste già, verrà eliminata e ricreata.
                # index=False evita di scrivere l'indice del DataFrame come colonna nel database.
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                logger.info(f"Dati da {csv_file_path.name} importati con successo nella tabella {table_name}")
            except Exception as e:
                # Se si verifica un errore durante l'importazione, lo registra.
                logger.error(f"Errore durante l'importazione del file {csv_file_path.name}: {e}", exc_info=True)

        # Registra il completamento dell'intero processo di importazione.
        logger.info(f"Processo di importazione completato")

    # Il blocco 'finally' viene eseguito sempre, sia che si verifichi un'eccezione o meno.
    finally:
        # Se la connessione al database è stata aperta, la chiude per rilasciare le risorse.
        if conn:
            conn.close()