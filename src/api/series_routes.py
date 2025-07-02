from fastapi import APIRouter, Query

from src.api.fetch_from_db import fetch_data_from_db
from src.configurations import config

router = APIRouter(prefix="/serie-calcolate", tags=["Serie Calcolate"])

@router.get("/media-occupazione-macroaree")
def get_media_occupazione_macroaree(
    da_anno: int | None = Query(None, description="Anno di inizio"),
    a_anno: int | None = Query(None, description= "Anno di fine")
):
    """
    Media Variazione percentuale occupazione delle 5 Aree.
    """
    return fetch_data_from_db(config.tabella_medie_macroaree_occupazione_pesca,da_anno,a_anno)


@router.get("/media-occupazione-nazionale")
def get_media_occupazione_nazionale(
    da_anno: int | None = Query(None, description="Anno di inizio"),
    a_anno: int | None = Query(None, description= "Anno di fine")
):
    """
    Media Variazione percentuale occupazione nazionale.
    """
    return fetch_data_from_db(config.tabella_media_nazionale_occupazione_pesca,da_anno,a_anno)


@router.get("/media-valore-aggiunto-macroaree")
def get_media_valore_aggiunto_macroaree(
    da_anno: int | None = Query(None, description="Anno di inizio"),
    a_anno: int | None = Query(None, description= "Anno di fine")
):
    """
    Media percentuale valore aggiunto per Macro-Area
    """
    return fetch_data_from_db(config.tabella_medie_macroaree_valore_aggiunto_pesca,da_anno,a_anno)


@router.get("/produttivita-macroaree")
def get_produttivita_macroaree(
    da_anno: int | None = Query(None, description="Anno di inizio"),
    a_anno: int | None = Query(None, description= "Anno di fine")
):
    """
    Produttività totale in migliaia di euro delle 5 Aree Nord-ovest, Nord-est, Centro, Sud, Isole.
    """
    return fetch_data_from_db(config.tabella_totali_macroaree_produttivita_pesca,da_anno,a_anno)


@router.get("/produttivita-nazionale")
def get_produttivita_nazionale(
    da_anno: int | None = Query(None, description="Anno di inizio"),
    a_anno: int | None = Query(None, description= "Anno di fine")
):
    """
    Produttività totale in migliaia di euro nazionale.
    """
    return fetch_data_from_db(config.tabella_totale_nazionale_produttivita_pesca,da_anno,a_anno)