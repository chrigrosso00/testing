from src.generate_plots.create_plots import crea_grafico_serie
from src.configurations import config
from src.logging.log_setup import get_logger

logger = get_logger(__name__)


def main():
    """
    Funzione principale per eseguire la generazione di tutti i grafici delle serie calcolate.
    """
    logger.info("--- Avvio dello script di generazione grafici ---")

    try:
        # --- Grafico 1: Media Variazione % Occupazione per Macro Aree ---
        logger.info("Generazione grafico: Media Variazione % Occupazione per Macroarea")
        crea_grafico_serie(
            table_name=config.tabella_medie_macroaree_occupazione_pesca,
            y_col=config.colonna_media_macroarea_variazione_percentuale_occupazione,
            color_col=config.colonna_macro_area,
            title="Media Variazione % Occupazione per Macroarea",
            y_axis_title="Variazione Percentuale (%)"
        )

        # --- Grafico 2: Media Variazione % Occupazione Nazionale ---
        logger.info("Generazione grafico: Media Variazione % Occupazione Nazionale")
        crea_grafico_serie(
            table_name=config.tabella_media_nazionale_occupazione_pesca,
            y_col=config.colonna_media_nazionale_variazione_percentuale_occupazione,
            title="Media Variazione % Occupazione Nazionale",
            y_axis_title="Variazione Percentuale (%)"
        )

        # --- Grafico 3: Produttività Totale per Macro Aree ---
        logger.info("Generazione grafico: Produttività Totale per Macroarea")
        crea_grafico_serie(
            table_name=config.tabella_totali_macroaree_produttivita_pesca,
            y_col=config.colonna_totale_macroarea_produttivita,
            color_col=config.colonna_macro_area,
            title="Produttività Totale per Macroarea",
            y_axis_title="Produttività Totale (migliaia di €)"
        )

        # --- Grafico 4: Produttività Totale Nazionale ---
        logger.info("Generazione grafico: Produttività Totale Nazionale")
        crea_grafico_serie(
            table_name=config.tabella_totale_nazionale_produttivita_pesca,
            y_col=config.colonna_totale_nazionale_produttivita,
            title="Produttività Totale Nazionale",
            y_axis_title="Produttività Totale (migliaia di €)"
        )

        # --- Grafico 5: Media % Valore Aggiunto per Macro Aree ---
        logger.info("Generazione grafico: Media % Valore Aggiunto per Macroarea")
        crea_grafico_serie(
            table_name=config.tabella_medie_macroaree_valore_aggiunto_pesca,
            y_col=config.colonna_media_macroarea_percentuale_valore_aggiunto,
            color_col=config.colonna_macro_area,
            title="Media % Valore Aggiunto per Macroarea",
            y_axis_title="Valore Aggiunto Medio (%)"
        )

        logger.info("--- Tutti i grafici sono stati generati con successo. ---")

    except Exception as e:
        logger.error(f"Si è verificato un errore imprevisto durante la generazione dei grafici: {e}", exc_info=True)
        logger.error("Lo script è stato interrotto.")


if __name__ == "__main__":
    main()
