# Importa APIRouter per creare un gruppo di rotte e Query per definire i parametri delle richieste.
from fastapi import APIRouter, Query
# Importa la funzione che si occupa di interrogare il database.
from src.api.fetch_from_db import fetch_data_from_db
# Importa le configurazioni, che contengono i nomi delle tabelle.
from src.configurations import config

# Crea un'istanza di APIRouter.
# 'prefix' aggiunge "/tabelle_originali" all'inizio di tutte le rotte definite in questo file.
# 'tags' raggruppa queste rotte sotto "Tabelle Originali" nella documentazione dell'API.
router = APIRouter(prefix="/tabelle_originali", tags=["Tabelle Originali"])

# Definisce un endpoint per ottenere i dati sull'andamento dell'occupazione.
@router.get("/andamento-occupazione")
def get_andamento_occupazione(
        # Definisce un parametro opzionale 'da_anno' per filtrare i dati per anno di inizio.
        da_anno: int | None = Query(None, description="Anno di inizio"),
        # Definisce un parametro opzionale 'a_anno' per filtrare i dati per anno di fine.
        a_anno: int | None = Query(None, description="Anno di fine")
):
    """
        Esporta la tabella 'Andamento-occupazione-del-settore-della-pesca-per-regione'.
    """
    # Chiama la funzione per recuperare i dati, specificando la tabella corretta
    # e passando i filtri per l'anno.
    return fetch_data_from_db(config.tabella_andamento_occupazione_pesca, da_anno, a_anno)

# Definisce un endpoint per ottenere i dati sull'importanza economica.
@router.get("/importanza-economica")
def get_importanza_economica(
        # Parametro opzionale per l'anno di inizio.
        da_anno: int | None = Query(None, description="Anno di inizio"),
        # Parametro opzionale per l'anno di fine.
        a_anno: int | None = Query(None, description="Anno di fine")
):
    """
        Esporta la tabella 'Importanza-economica-del-settore-della-pesca-per-regione'.
        """
    # Recupera i dati dalla tabella sull'importanza economica.
    return fetch_data_from_db(config.tabella_importanza_economica_pesca, da_anno, a_anno)

# Definisce un endpoint per ottenere i dati sulla produttività.
@router.get("/produttivita")
def get_produttivita(
        # Parametro opzionale per l'anno di inizio.
        da_anno: int | None = Query(None, description="Anno di inizio"),
        # Parametro opzionale per l'anno di fine.
        a_anno: int | None = Query(None, description="Anno di fine")
):
    """
        Esporta la tabella 'Produttivita-del-settore-della-pesca-per-regione'.
        """
    # Recupera i dati dalla tabella sulla produttività.
    return fetch_data_from_db(config.tabella_produttivita_pesca, da_anno, a_anno)