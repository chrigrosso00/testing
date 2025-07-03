# Importa la funzione 'csv_to_sql' dal modulo db_operations, che gestisce l'importazione dei dati.
from src.database.db_operations import csv_to_sql
# Importa la funzione per ottenere un'istanza del logger.
from src.logging.log_setup import get_logger

# Inizializza il logger per questo modulo.
# Usare __name__ è una convenzione per avere log che indicano chiaramente da quale file provengono.
logger = get_logger(__name__)


# Definisce la funzione principale dello script.
def main():
    """
    Funzione principale che avvia il processo di importazione.
    """
    # Logga un messaggio per indicare l'inizio del processo.
    logger.info("Avvio dello script di importazione dati da CSV a database SQLite...")
    # Chiama la funzione che esegue l'importazione dei dati dai file CSV al database.
    csv_to_sql()
    # Logga un messaggio per indicare il completamento del processo.
    logger.info("Script di importazione terminato.")


# Questo blocco di codice viene eseguito solo se lo script è lanciato direttamente
# (es. 'python run_import.py') e non quando viene importato come modulo in un altro script.
if __name__ == "__main__":
    # Chiama la funzione principale per avviare l'esecuzione.
    main()