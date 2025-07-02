import logging
from pathlib import Path

PRJ_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PRJ_ROOT / "data"
DB_DIR = PRJ_ROOT / "database.db"

# --- Nomi Tabelle ---

tabella_andamento_occupazione_pesca = "Andamento-occupazione-del-settore-della-pesca-per-regione"
tabella_importanza_economica_pesca = "Importanza-economica-del-settore-della-pesca-per-regione"
tabella_produttivita_pesca = "Produttivita-del-settore-della-pesca-per-regione"

# --- Nomi Colonne ---

colonna_anno = "Anno"
colonna_regione = "Regione"
colonna_macro_area = "Macro Area"
colonna_variazione_percentuale = "Variazione percentuale unita di lavoro della pesca"
colonna_percentuale_valore_aggiunto = "Percentuale valore aggiunto pesca-piscicoltura-servizi"
colonna_produttivita = "Produttivita in migliaia di euro"

# --- Serie Calcolate ---

# 1. Produttività totale per Macro Aree
tabella_totali_macroaree_produttivita_pesca = "Produttivita_Totale_MacroAree_Pesca"
colonna_totale_macroarea_produttivita = "Produttivita_Totale_Macroarea_Migliaia_Euro"

# 2. Produttività totale Nazionale
tabella_totale_nazionale_produttivita_pesca = "Produttivita_Totale_Nazionale_Pesca"
colonna_totale_nazionale_produttivita = "Produttivita_Totale_Nazionale_Migliaia_Euro"

# 3. Media percentuale valore aggiunto per Macro Aree
tabella_medie_macroaree_valore_aggiunto_pesca = "Medie_Macroaree_Valore_Aggiunto_Pesca"
colonna_media_macroarea_percentuale_valore_aggiunto = "Media_Macroarea_Percentuale_Valore_Aggiunto"

# 4. Media Variazione percentuale occupazione Nazionale
tabella_media_nazionale_occupazione_pesca = "Media_Nazionale_Andamento_Occupazione_Pesca"
colonna_media_nazionale_variazione_percentuale_occupazione = "Media_Nazionale_Variazione_Percentuale_Occupazione"

# 5. Media Variazione percentuale occupazione per Macro Aree
tabella_medie_macroaree_occupazione_pesca = "Medie_Macroaree_Andamento_Occupazione_Pesca"
colonna_media_macroarea_variazione_percentuale_occupazione = "Media_Macroarea_Variazione_Percentuale_Occupazione"

# --- Macro-Aree ---
macro_aree = {
    'Valle d\'Aosta': 'Nord-ovest', 'Piemonte': 'Nord-ovest', 'Liguria': 'Nord-ovest', 'Lombardia': 'Nord-ovest',
    'Trentino-Alto Adige': 'Nord-est', 'Veneto': 'Nord-est', 'Friuli-Venezia Giulia': 'Nord-est',
    'Emilia-Romagna': 'Nord-est',
    'Toscana': 'Centro', 'Umbria': 'Centro', 'Marche': 'Centro', 'Lazio': 'Centro', 'Abruzzo': 'Centro',
    'Molise': 'Sud', 'Campania': 'Sud', 'Puglia': 'Sud', 'Basilicata': 'Sud', 'Calabria': 'Sud',
    'Sicilia': 'Isole', 'Sardegna': 'Isole'
}

# --- Logging ---

log_dir_name = "logs"
log_path = PRJ_ROOT / log_dir_name
log_filename = "app.log"
log_file_path = log_path / log_filename
log_level = logging.INFO
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
