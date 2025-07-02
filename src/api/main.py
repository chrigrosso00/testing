import uvicorn
from fastapi import FastAPI

from src.api import table_routes, series_routes
from src.configurations import config
from src.logging.log_setup import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="API dati di Pesca",
    version="1.0",
    description="API per l'esportazione di dati di Pesca e Serie Calcolate",
)

app.include_router(table_routes.router)
app.include_router(series_routes.router)


@app.get("/", tags=["root"])
async def read_root():
    logger.info(f"Root dell'API avviata")
    return {
        "message": "Benvenuto nell'API di dati di esca, consulta /docs per la interrogare il database ed esportare i dati"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=config.log_level)
