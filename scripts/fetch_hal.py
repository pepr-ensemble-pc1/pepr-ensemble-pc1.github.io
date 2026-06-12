#!/usr/bin/env python3
import requests
import json
import os
# Chemin absolu vers la racine du dépôt

API_URL = "https://api.archives-ouvertes.fr/search"

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(REPO_ROOT, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "hal_pepr_cats_articles.json")
params = {
    "q": "*:*",                          # Tous les documents
    "fq": [
        "collCode_s:PEPR-ENSEMBLE",      # ✅ Filtre par la collection PEPR-ENSEMBLE
        'anrProjectAcronym_s:"CATS"'     # ✅ Filtre par l'acronyme du projet
    ],
    "wt": "json",
    "fl": "*",                           # Tous les champs
    "rows": 1000
}

# Crée le dossier data s'il n'existe pas
os.makedirs(DATA_DIR, exist_ok=True)
response = requests.get(API_URL, params=params).json()
docs = response["response"]["docs"]


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(response, f, indent=2, ensure_ascii=False)

print(f"✅ {len(docs)} articles trouvés (collection: PEPR-ENSEMBLE, projet: CATS) → {OUTPUT_FILE}")
