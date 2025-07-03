# Importa il modulo 'logging' di Python per la gestione dei log.
import logging

# Importa l'oggetto di configurazione per accedere a impostazioni come il percorso dei log e il livello di log.
from src.configurations import config


# Definisce una funzione per configurare il sistema di logging dell'intera applicazione.
def setup_logging():
    # Assicura che la cartella specificata per i file di log esista, creandola se necessario.
    # 'exist_ok=True' evita che venga sollevato un errore se la cartella esiste già.
    config.log_path.mkdir(exist_ok=True)

    # Configura il logger di root. Questa è una configurazione globale.
    logging.basicConfig(
        # Imposta il livello minimo di severità dei messaggi da registrare (es. DEBUG, INFO, WARNING).
        level=config.log_level,
        # Definisce il formato dei messaggi di log (es. timestamp, nome del logger, messaggio).
        format=config.log_format,
        # Specifica dove inviare i messaggi di log.
        handlers=[
            # Un handler per scrivere i log su un file.
            logging.FileHandler(config.log_file_path),
            # Un handler per stampare i log sulla console (terminale).
            logging.StreamHandler()
        ]
    )


# Definisce una funzione di utilità per ottenere un'istanza di logger specifica per un modulo.
def get_logger(name: str) -> logging.getLogger:
    """
    Restituisce un logger con un nome specifico.
    È una buona pratica usare __name__ come nome, in modo che il logger rifletta il nome del modulo.
    """
    # Restituisce un logger. Se un logger con questo nome esiste già, restituisce quello, altrimenti ne crea uno nuovo.
    return logging.getLogger(name)


# Chiama la funzione di configurazione all'avvio del modulo.
# Questo assicura che il logging sia configurato non appena questo file viene importato per la prima volta.
setup_logging()
