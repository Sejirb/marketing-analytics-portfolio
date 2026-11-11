-- 3. Rétention par cohorte mensuelle d'acquisition
-- Pour chaque cohorte (mois du premier achat), part des clients qui recommandent
-- N mois plus tard (N = 1 à 12).
WITH commandes AS (
    SELECT
        c.customer_unique_id,
        CAST(STRFTIME('%Y', o.order_purchase_timestamp) AS INTEGER) * 12
            + CAST(STRFTIME('%m', o.order_purchase_timestamp) AS INTEGER) AS index_mois,
        STRFTIME('%Y-%m', o.order_purchase_timestamp) AS mois
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
      AND o.order_purchase_timestamp >= '2017-01-01'
      AND o.order_purchase_timestamp < '2018-09-01'
),
premier_achat AS (
    SELECT customer_unique_id, MIN(index_mois) AS index_cohorte, MIN(mois) AS cohorte
    FROM commandes
    GROUP BY customer_unique_id
),
taille_cohorte AS (
    SELECT cohorte, COUNT(*) AS clients_cohorte
    FROM premier_achat
    GROUP BY cohorte
)
SELECT
    pa.cohorte,
    t.clients_cohorte,
    co.index_mois - pa.index_cohorte AS mois_ecoules,
    COUNT(DISTINCT co.customer_unique_id) AS clients_actifs,
    ROUND(COUNT(DISTINCT co.customer_unique_id) * 100.0 / t.clients_cohorte, 2) AS taux_retention
FROM commandes co
JOIN premier_achat pa ON pa.customer_unique_id = co.customer_unique_id
JOIN taille_cohorte t ON t.cohorte = pa.cohorte
WHERE co.index_mois - pa.index_cohorte BETWEEN 1 AND 12
GROUP BY pa.cohorte, t.clients_cohorte, mois_ecoules
ORDER BY pa.cohorte, mois_ecoules;
