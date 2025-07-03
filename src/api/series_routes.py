# Importa APIRouter per creare un gruppo di rotte e Query per definire i parametri delle richieste.
from fastapi import APIRouter, Query

# Importa la funzione che si occupa di interrogare il database.
from src.api.fetch_from_db import fetch_data_from_db
# Importa le configurazioni, che contengono i nomi delle tabelle.
from src.configurations import config

# Crea un'istanza di APIRouter.
# 'prefix' aggiunge "/serie-calcolate" all'inizio di tutte le rotte definite in questo file.
# 'tags' raggruppa queste rotte sotto "Serie Calcolate" nella documentazione dell'API.
router = APIRouter(prefix="/serie-calcolate", tags=["Serie Calcolate"])


# Definisce un endpoint per ottenere la media di occupazione per macroaree.
@router.get("/media-occupazione-macroaree")
def get_media_occupazione_macroaree(
    # Definisce un parametro opzionale 'da_anno' per filtrare i dati.
    da_anno: int | None = Query(None, description="Anno di inizio"),
    # Definisce un parametro opzionale 'a_anno' per filtrare i dati.
    a_anno: int | None = Query(None, description="Anno di fine")
):
    """
    Media Variazione percentuale occupazione delle 5 Aree.
    """
    # Chiama la funzione generica per recuperare i dati, specificando la tabella corretta
    # e passando i filtri per l'anno.
    return fetch_data_from_db(config.tabella_medie_macroaree_occupazione_pesca, da_anno, a_anno)


# Definisce un endpoint per ottenere la media di occupazione a livello nazionale.
@router.get("/media-occupazione-nazionale")
def get_media_occupazione_nazionale(
    da_anno: int | None = Query(None, description="Anno di inizio"),
    a_anno: int | None = Query(None, description="Anno di fine")
):
    """
    Media Variazione percentuale occupazione nazionale.
    """
    # Recupera i dati dalla tabella della media nazionale di occupazione.
    return fetch_data_from_db(config.tabella_media_nazionale_occupazione_pesca, da_anno, a_anno)


# Definisce un endpoint per ottenere la media del valore aggiunto per macroaree.
@router.get("/media-valore-aggiunto-macroaree")
def get_media_valore_aggiunto_macroaree(
    da_anno: int | None = Query(None, description="Anno di inizio"),
    a_anno: int | None = Query(None, description="Anno di fine")
):
    """
    Media percentuale valore aggiunto per Macro-Area
    """
    # Recupera i dati dalla tabella delle medie del valore aggiunto per macroarea.
    return fetch_data_from_db(config.tabella_medie_macroaree_valore_aggiunto_pesca, da_anno, a_anno)


# Definisce un endpoint per ottenere la produttività per macroaree.
@router.get("/produttivita-macroaree")
def get_produttivita_macroaree(
    da_anno: int | None = Query(None, description="Anno di inizio"),
    a_anno: int | None = Query(None, description="Anno di fine")
):
    """
    Produttività totale in migliaia di euro delle 5 Aree Nord-ovest, Nord-est, Centro, Sud, Isole.
    """
    # Recupera i dati dalla tabella dei totali di produttività per macroarea.
    return fetch_data_from_db(config.tabella_totali_macroaree_produttivita_pesca, da_anno, a_anno)


# Definisce un endpoint per ottenere la produttività a livello nazionale.
@router.get("/produttivita-nazionale")
def get_produttivita_nazionale(
    da_anno: int | None = Query(None, description="Anno di inizio"),
    a_anno: int | None = Query(None, description="Anno di fine")
):
    """
    Produttività totale in migliaia di euro nazionale.
    """
    # Recupera i dati dalla tabella del totale di produttività nazionale.
    return fetch_data_from_db(config.tabella_totale_nazionale_produttivita_pesca, da_anno, a_anno)