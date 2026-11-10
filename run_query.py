import sqlite3
import pandas as pd

# Afficher toutes les colonnes proprement sans coupure
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

conn = sqlite3.connect("olist_ecommerce.db")

query = """
SELECT 
    STRFTIME('%Y-%m', o.order_purchase_timestamp) AS mois,
    COUNT(DISTINCT o.order_id) AS total_commandes,
    ROUND(SUM(p.payment_value), 2) AS chiffre_affaires,
    ROUND(AVG(p.payment_value), 2) AS panier_moyen
FROM orders o
JOIN payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
  AND o.order_purchase_timestamp >= '2017-01-01'
  AND o.order_purchase_timestamp < '2018-09-01'
GROUP BY mois
ORDER BY mois ASC;
"""

df_result = pd.read_sql_query(query, conn)
print(df_result)

conn.close()