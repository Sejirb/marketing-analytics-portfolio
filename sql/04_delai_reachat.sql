-- 4. Délai entre la première et la deuxième commande
-- Sert à choisir le moment d'une relance CRM. Attention : une part importante
-- des « réachats » a lieu le jour même (commande fractionnée, pas une vraie fidélité).
WITH commandes_ordonnees AS (
    SELECT
        c.customer_unique_id,
        o.order_purchase_timestamp,
        ROW_NUMBER() OVER (
            PARTITION BY c.customer_unique_id
            ORDER BY o.order_purchase_timestamp
        ) AS rang
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
),
delais AS (
    SELECT
        JULIANDAY(c2.order_purchase_timestamp) - JULIANDAY(c1.order_purchase_timestamp) AS jours
    FROM commandes_ordonnees c1
    JOIN commandes_ordonnees c2
      ON c2.customer_unique_id = c1.customer_unique_id
     AND c1.rang = 1
     AND c2.rang = 2
),
tranches AS (
    SELECT
        CASE
            WHEN jours < 1 THEN 1
            WHEN jours <= 30 THEN 2
            WHEN jours <= 90 THEN 3
            WHEN jours <= 180 THEN 4
            WHEN jours <= 365 THEN 5
            ELSE 6
        END AS ordre,
        CASE
            WHEN jours < 1 THEN 'Même jour'
            WHEN jours <= 30 THEN '1 à 30 jours'
            WHEN jours <= 90 THEN '31 à 90 jours'
            WHEN jours <= 180 THEN '91 à 180 jours'
            WHEN jours <= 365 THEN '181 à 365 jours'
            ELSE 'Plus de 365 jours'
        END AS delai
    FROM delais
)
SELECT
    delai,
    COUNT(*) AS clients,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM delais), 1) AS part_pourcentage
FROM tranches
GROUP BY ordre, delai
ORDER BY ordre;
