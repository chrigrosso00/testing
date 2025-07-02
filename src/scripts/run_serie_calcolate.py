from src.logging.log_setup import get_logger
from src.serie_calcolate.calcolo_media_occupazione_macroaree import calcola_media_occupazione_macroaree
from src.serie_calcolate.calcolo_media_occupazione_nazionale import calcola_media_occupazione_nazionale
from src.serie_calcolate.calcolo_media_valore_aggiunto_macroaree import calcola_media_valore_aggiunto_macroaree
from src.serie_calcolate.calcolo_produttivita_macroaree import calcola_produttivita_macroaree
from src.serie_calcolate.calcolo_produttivita_nazionale import calcola_produttivita_nazionale

logger = get_logger(__name__)


def main():
    logger.info(f"Avvio del processo di calcolo delle serie c   alcolate...")

    try:
        calcola_media_occupazione_macroaree()
        calcola_media_occupazione_nazionale()
        calcola_media_valore_aggiunto_macroaree()
        calcola_produttivita_macroaree()
        calcola_produttivita_nazionale()
        logger.info(f"Processo di calcolo delle serie calcolate completato.")
    except Exception as e:
        logger.error(f"Errore durante il processo di calcolo delle serie calcolate: {e}", exc_info=True)


if __name__ == "__main__":
    main()
