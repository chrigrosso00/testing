from fastapi import APIRouter, Query
from src.api.fetch_from_db import fetch_data_from_db
from src.configurations import config


router = APIRouter(prefix="/tabelle_originali", tags=["Tabelle Originali"])

@router.get("/andamento-occupazione")
def get_andamento_occupazione(
        da_anno: int | None = Query(None, description="Anno di inizio"),
        a_anno: int | None = Query(None, description="Anno di fine")
):
    """
        Esporta la tabella 'Andamento-occupazione-del-settore-della-pesca-per-regione'.
    """
    return fetch_data_from_db(config.tabella_andamento_occupazione_pesca, da_anno, a_anno)

@router.get("/importanza-economica")
def get_importanza_economica(
        da_anno: int | None = Query(None, description="Anno di inizio"),
        a_anno: int | None = Query(None, description="Anno di fine")
):
    """
        Esporta la tabella 'Importanza-economica-del-settore-della-pesca-per-regione'.
        """
    return fetch_data_from_db(config.tabella_importanza_economica_pesca, da_anno, a_anno)

@router.get("/produttivita")
def get_produttivita(
        da_anno: int | None = Query(None, description="Anno di inizio"),
        a_anno: int | None = Query(None, description="Anno di fine")
):
    """
        Esporta la tabella 'Produttivita-del-settore-della-pesca-per-regione'.
        """
    return fetch_data_from_db(config.tabella_produttivita_pesca, da_anno, a_anno)
