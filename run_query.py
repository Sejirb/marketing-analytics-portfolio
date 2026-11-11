"""Exécute les requêtes du dossier sql/ et exporte chaque résultat en CSV dans results/.

Usage :
    python run_query.py            # toutes les requêtes
    python run_query.py 03 07      # seulement celles dont le nom commence par 03 ou 07
"""
import sqlite3
import sys
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parent
CHEMIN_DB = RACINE / "olist_ecommerce.db"
DOSSIER_SQL = RACINE / "sql"
DOSSIER_RESULTATS = RACINE / "results"

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def main():
    if not CHEMIN_DB.exists():
        print("Base introuvable : lancez d'abord `python setup_db.py`.")
        sys.exit(1)

    prefixes = tuple(sys.argv[1:])
    fichiers = sorted(DOSSIER_SQL.glob("*.sql"))
    if prefixes:
        fichiers = [f for f in fichiers if f.name.startswith(prefixes)]
    if not fichiers:
        print("Aucune requête ne correspond.")
        sys.exit(1)

    DOSSIER_RESULTATS.mkdir(exist_ok=True)
    with sqlite3.connect(CHEMIN_DB) as conn:
        for fichier in fichiers:
            resultat = pd.read_sql_query(fichier.read_text(encoding="utf-8"), conn)
            sortie = DOSSIER_RESULTATS / f"{fichier.stem}.csv"
            resultat.to_csv(sortie, index=False)
            print(f"\n=== {fichier.name} ({len(resultat)} lignes) -> results/{sortie.name} ===")
            print(resultat.to_string(index=False))


if __name__ == "__main__":
    main()
