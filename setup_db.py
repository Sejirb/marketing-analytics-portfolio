import os
import sqlite3
import pandas as pd

# Connexion / création de la base de données locale
conn = sqlite3.connect("olist_ecommerce.db")
cursor = conn.cursor()

# Chemins des fichiers CSV
files = {
    "orders": "data/olist_orders_dataset.csv",
    "payments": "data/olist_order_payments_dataset.csv",
    "customers": "data/olist_customers_dataset.csv",
}

for table_name, file_path in files.items():
    if os.path.exists(file_path):
        print(f"Chargement de {table_name}...")
        df = pd.read_csv(file_path)
        # Insertion des données dans la base SQLite
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"-> Table '{table_name}' chargée avec {len(df)} lignes.")
    else:
        print(f"Fichier non trouvé : {file_path}")

conn.close()
print("Base de données créée avec succès dans 'olist_ecommerce.db' !")