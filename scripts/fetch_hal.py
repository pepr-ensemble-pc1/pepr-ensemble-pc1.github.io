#!/usr/bin/env python3
import requests
import json
import os

API_URL = "https://api.archives-ouvertes.fr/search"
OUTPUT_FILE = "data/hal_pepr_cats_articles.json"

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

response = requests.get(API_URL, params=params).json()
docs = response["response"]["docs"]

# Sauvegarde
os.makedirs("data", exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(response, f, indent=2, ensure_ascii=False)

print(f"✅ {len(docs)} articles trouvés (collection: PEPR-ENSEMBLE, projet: CATS) → {OUTPUT_FILE}")