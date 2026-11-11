-- 2. Taux de réachat : quelle proportion de clients commande plus d'une fois ?
-- customer_id change à chaque commande dans Olist : le vrai identifiant client
-- est customer_unique_id.
WITH commandes_par_client AS (
    SELECT
        c.customer_unique_id,
        COUNT(o.order_id) AS nb_commandes
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT
    nb_commandes,
    COUNT(*) AS volume_clients,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM commandes_par_client), 2) AS part_pourcentage
FROM commandes_par_client
GROUP BY nb_commandes
ORDER BY nb_commandes;
