# src/scripts/run_serie_calcolate.py

# Importa la funzione per ottenere un'istanza del logger.
from src.logging.log_setup import get_logger

# Importa tutte le funzioni di calcolo delle serie derivate.
# Ogni funzione è responsabile del calcolo di una specifica metrica
from src.serie_calcolate.calcolo_media_occupazione_macroaree import calcola_media_occupazione_macroaree
from src.serie_calcolate.calcolo_media_occupazione_nazionale import calcola_media_occupazione_nazionale
from src.serie_calcolate.calcolo_media_valore_aggiunto_macroaree import calcola_media_valore_aggiunto_macroaree
from src.serie_calcolate.calcolo_produttivita_macroaree import calcola_produttivita_macroaree
from src.serie_calcolate.calcolo_produttivita_nazionale import calcola_produttivita_nazionale

# Inizializza il logger per questo modulo.
logger = get_logger(__name__)


# Definisce la funzione principale dello script.
def main():
    """
    Funzione principale che orchestra il calcolo di tutte le serie derivate.
    """
    # Logga un messaggio per indicare l'inizio del processo.
    logger.info("Avvio del processo di calcolo delle serie calcolate...")

    # Utilizza un blocco try...except per catturare eventuali errori durante l'esecuzione dei calcoli.
    try:
        # Chiama in sequenza ogni funzione di calcolo.
        # Ognuna di queste funzioni legge i dati dal database, esegue i calcoli
        # e salva i risultati in una nuova tabella.
        calcola_media_occupazione_macroaree()
        calcola_media_occupazione_nazionale()
        calcola_media_valore_aggiunto_macroaree()
        calcola_produttivita_macroaree()
        calcola_produttivita_nazionale()

        # Logga un messaggio di successo al termine di tutti i calcoli.
        logger.info("Processo di calcolo delle serie calcolate completato.")

    # Cattura qualsiasi eccezione generica che potrebbe verificarsi durante i calcoli.
    except Exception as e:
        # Logga un messaggio di errore dettagliato, includendo la traccia dell'errore,
        # per facilitare il debug.
        logger.error(f"Errore durante il processo di calcolo delle serie calcolate: {e}", exc_info=True)


# Questo blocco viene eseguito solo se lo script è lanciato direttamente
# (es. 'python run_serie_calcolate.py').
if __name__ == "__main__":
    # Chiama la funzione principale per avviare l'esecuzione.
    main()