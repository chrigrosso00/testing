# Importa la funzione per creare i grafici.
from src.generate_plots.create_plots import crea_grafico_serie
# Importa le configurazioni (nomi di tabelle, colonne, ecc.).
from src.configurations import config
# Importa la funzione per ottenere un'istanza del logger.
from src.logging.log_setup import get_logger

# Inizializza il logger per questo modulo.
logger = get_logger(__name__)


# Definisce la funzione principale dello script.
def main():
    """
    Funzione principale per eseguire la generazione di tutti i grafici delle serie calcolate.
    """
    # Logga un messaggio per indicare l'inizio dell'esecuzione dello script.
    logger.info("--- Avvio dello script di generazione grafici ---")

    # Utilizza un blocco try...except per catturare eventuali errori durante la generazione dei grafici.
    try:
        # --- Grafico 1: Media Variazione % Occupazione per Macro Aree ---
        # Logga l'inizio della generazione del primo grafico.
        logger.info("Generazione grafico: Media Variazione % Occupazione per Macroarea")
        # Chiama la funzione per creare il grafico, passando i parametri specifici.
        crea_grafico_serie(
            table_name=config.tabella_medie_macroaree_occupazione_pesca,
            y_col=config.colonna_media_macroarea_variazione_percentuale_occupazione,
            color_col=config.colonna_macro_area,  # Usa la macro area per differenziare le linee con colori diversi.
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
            color_col=config.colonna_macro_area,  # Usa la macro area per i colori.
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
            color_col=config.colonna_macro_area,  # Usa la macro area per i colori.
            title="Media % Valore Aggiunto per Macroarea",
            y_axis_title="Valore Aggiunto Medio (%)"
        )

        # Logga un messaggio di successo al termine della generazione di tutti i grafici.
        logger.info("--- Tutti i grafici sono stati generati con successo. ---")

    # Cattura qualsiasi eccezione generica che potrebbe verificarsi.
    except Exception as e:
        # Logga un messaggio di errore dettagliato, includendo la traccia dell'errore.
        logger.error(f"Si è verificato un errore imprevisto durante la generazione dei grafici: {e}", exc_info=True)
        logger.error("Lo script è stato interrotto.")


# Questo blocco viene eseguito solo se lo script è lanciato direttamente.
if __name__ == "__main__":
    # Chiama la funzione principale per avviare la generazione dei grafici.
    main()