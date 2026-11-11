"""Crée la base SQLite locale à partir des fichiers CSV Olist placés dans data/."""
import sqlite3
import sys
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parent
DOSSIER_DATA = RACINE / "data"
CHEMIN_DB = RACINE / "olist_ecommerce.db"

# Table SQLite -> fichier CSV source
TABLES = {
    "orders": "olist_orders_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

# Index sur les clés de jointure utilisées par les requêtes
INDEX = [
    ("orders", "order_id"),
    ("orders", "customer_id"),
    ("payments", "order_id"),
    ("customers", "customer_id"),
    ("customers", "customer_unique_id"),
    ("order_items", "order_id"),
    ("order_items", "product_id"),
    ("reviews", "order_id"),
    ("products", "product_id"),
]


def main():
    manquants = [f for f in TABLES.values() if not (DOSSIER_DATA / f).exists()]
    if manquants:
        print("Fichiers introuvables dans data/ :")
        for fichier in manquants:
            print(f"  - {fichier}")
        print("Téléchargez le dataset Olist (voir README) et décompressez-le dans data/.")
        sys.exit(1)

    with sqlite3.connect(CHEMIN_DB) as conn:
        for table, fichier in TABLES.items():
            # utf-8-sig : le fichier de traduction des catégories commence par un BOM
            df = pd.read_csv(DOSSIER_DATA / fichier, encoding="utf-8-sig")
            df.to_sql(table, conn, if_exists="replace", index=False)
            print(f"Table '{table}' chargée : {len(df):,} lignes".replace(",", " "))

        for table, colonne in INDEX:
            conn.execute(
                f"CREATE INDEX IF NOT EXISTS idx_{table}_{colonne} ON {table} ({colonne})"
            )

    print(f"Base de données créée : {CHEMIN_DB.name}")


if __name__ == "__main__":
    main()
