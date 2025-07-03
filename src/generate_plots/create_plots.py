# Importa Optional per definire tipi di argomenti che possono essere None.
from typing import Optional
# Importa pandas per la manipolazione dei dati, in particolare per creare DataFrame.
import pandas as pd
# Importa plotly.express per creare grafici interattivi in modo semplice.
import plotly.express as px

# Importa la funzione per recuperare i dati dal database.
from src.api.fetch_from_db import fetch_data_from_db
# Importa le configurazioni per accedere a valori condivisi come nomi di colonne e tabelle.
from src.configurations import config
# Importa la funzione per inizializzare il logger.
from src.logging.log_setup import get_logger

# Inizializza il logger per questo modulo, per registrare eventi e informazioni.
logger = get_logger(__name__)


# Definisce una funzione per creare un grafico a linee da una serie di dati.
def crea_grafico_serie(
        table_name: str,
        y_col: str,
        title: str,
        color_col: Optional[str] = None,
        y_axis_title: Optional[str] = None
):
    """
        Crea e visualizza un grafico a linee per una serie storica.

        Args:
            table_name (str): Il nome della tabella da cui recuperare i dati.
            y_col (str): Il nome della colonna da usare per l'asse Y.
            title (str): Il titolo del grafico.
            color_col (str, optional): Il nome della colonna da usare per differenziare le linee (es. per macroarea).
            y_axis_title (str, optional): Il titolo per l'asse Y. Se non fornito, usa y_col.
    """
    # Registra l'inizio del processo di creazione del grafico.
    logger.info(f"Inizio creazione del grafico per la tabella '{table_name}'")
    # Usa un blocco try...except per gestire eventuali errori durante il processo.
    try:
        # Recupera tutti i dati dalla tabella specificata, senza filtri di anno.
        data = fetch_data_from_db(table_name, da_anno=None, a_anno=None)
        # Se non vengono restituiti dati, registra un avviso e interrompe la funzione.
        if not data:
            logger.warning(f"Nessun dato trovato per la tabella '{table_name}'")
            return
        # Converte la lista di dizionari (dati) in un DataFrame di pandas.
        df = pd.DataFrame(data)
        # Crea un grafico a linee utilizzando plotly.express.
        fig = px.line(
            df,  # Il DataFrame contenente i dati.
            x=config.colonna_anno,  # Colonna per l'asse X (l'anno).
            y=y_col,  # Colonna per l'asse Y (il valore da plottare).
            color=color_col,  # Colonna per differenziare le linee con colori diversi (opzionale).
            title=title,  # Titolo del grafico.
            labels={  # Etichette personalizzate per gli assi.
                config.colonna_anno: "Anno",
                y_col: y_axis_title or y_col  # Usa il titolo personalizzato se fornito, altrimenti il nome della colonna.
            },
            markers=True  # Mostra un marcatore per ogni punto dati sulla linea.
        )
        # Aggiorna ulteriormente il layout del grafico.
        fig.update_layout(
            xaxis_title="Anno",  # Titolo dell'asse X.
            yaxis_title=y_axis_title or y_col,  # Titolo dell'asse Y.
            # Imposta il titolo della legenda se si usano colori diversi, altrimenti lo lascia vuoto.
            legend_title_text=config.colonna_macro_area if color_col else ""
        )
        # Registra che il grafico sta per essere visualizzato.
        logger.info(f"Visualizzazione grafico: {title}")
        # Mostra il grafico interattivo (di solito apre una nuova finestra o un tab nel browser).
        fig.show()

    # Cattura qualsiasi eccezione che si possa verificare nel blocco 'try'.
    except Exception as e:
        # Registra un messaggio di errore dettagliato, includendo la traccia dell'errore.
        logger.error(f"Errore durante la creazione del grafico per {table_name}: {e}", exc_info=True)
        # Fornisce un suggerimento utile all'utente per risolvere il problema.
        logger.error(
            f"Controlla che i nomi delle colonne ({y_col, {color_col} }) siano corretti e presenti nella tabella '{table_name}'")
