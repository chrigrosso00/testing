# Importa uvicorn, che è un server ASGI (Asynchronous Server Gateway Interface) per eseguire l'applicazione.
import uvicorn
# Importa la classe principale FastAPI per creare l'API.
from fastapi import FastAPI

# Importa i router definiti in altri file per organizzare gli endpoint.
from src.api import table_routes, series_routes
# Importa le configurazioni dell'applicazione (es. livello di log).
from src.configurations import config
# Importa la funzione per impostare il logger.
from src.logging.log_setup import get_logger

# Inizializza il logger per questo modulo, per registrare eventi e informazioni.
logger = get_logger(__name__)

# Crea un'istanza dell'applicazione FastAPI.
# Vengono forniti metadati come titolo, versione e descrizione, che saranno visibili nella documentazione automatica (es. /docs).
app = FastAPI(
    title="API dati di Pesca",
    version="1.0",
    description="API per l'esportazione di dati di Pesca e Serie Calcolate",
)

# Include il router per le rotte relative alle tabelle del database.
# Tutti gli endpoint definiti in 'table_routes' saranno disponibili sotto l'applicazione principale.
app.include_router(table_routes.router)
# Include il router per le rotte relative alle serie calcolate.
app.include_router(series_routes.router)


# Definisce un endpoint per la radice ("/") dell'API.
# 'tags' aiuta a raggruppare gli endpoint nella documentazione.
@app.get("/", tags=["root"])
async def read_root():
    """
    Endpoint di benvenuto dell'API.
    """
    # Registra un messaggio informativo ogni volta che questo endpoint viene chiamato.
    logger.info(f"Root dell'API avviata")
    # Restituisce un messaggio JSON di benvenuto.
    return {
        "message": "Benvenuto nell'API di dati di esca, consulta /docs per la interrogare il database ed esportare i dati"}


# Questo blocco di codice viene eseguito solo se lo script è lanciato direttamente (es. 'python main.py').
# Non viene eseguito se il modulo è importato da un altro script.
if __name__ == "__main__":
    # Avvia il server uvicorn per servire l'applicazione FastAPI.
    # 'host="0.0.0.0"' rende il server accessibile da altre macchine sulla rete.
    # 'port=8000' imposta la porta su cui il server ascolterà.
    # 'log_level' imposta il livello di verbosità dei log del server, preso dalla configurazione.
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=config.log_level)