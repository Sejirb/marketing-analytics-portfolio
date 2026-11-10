-- ==========================================================
-- ANALYSE DE LA VALEUR CLIENT & RÉTENTION (DATASET OLIST)
-- ==========================================================

-- 1. Évolution du volume de commandes et chiffre d'affaires mensuel
SELECT 
    STRFTIME('%Y-%m', order_purchase_timestamp) AS mois,
    COUNT(DISTINCT order_id) AS total_commandes
FROM orders
WHERE order_status = 'delivered'
GROUP BY mois
ORDER BY mois ASC;

-- 2. Taux de réachat : Quelle proportion de clients commande plus d'une fois ?
WITH commandes_par_client AS (
    SELECT 
        c.customer_unique_id,
        COUNT(o.order_id) AS nb_commandes
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT 
    nb_commandes,
    COUNT(customer_unique_id) AS volume_clients,
    ROUND(COUNT(customer_unique_id) * 100.0 / (SELECT COUNT(*) FROM commandes_par_client), 2) AS part_pourcentage
FROM commandes_par_client
GROUP BY nb_commandes
ORDER BY nb_commandes ASC;