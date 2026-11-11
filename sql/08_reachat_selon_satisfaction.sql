-- 8. Le réachat dépend-il de la satisfaction sur la première commande ?
-- Taux de clients ayant recommandé, selon la note laissée sur leur première commande.
WITH commandes_ordonnees AS (
    SELECT
        c.customer_unique_id,
        o.order_id,
        ROW_NUMBER() OVER (
            PARTITION BY c.customer_unique_id
            ORDER BY o.order_purchase_timestamp
        ) AS rang,
        COUNT(*) OVER (PARTITION BY c.customer_unique_id) AS nb_commandes
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
),
note_par_commande AS (
    SELECT order_id, AVG(review_score) AS note
    FROM reviews
    GROUP BY order_id
)
SELECT
    CAST(ROUND(n.note) AS INTEGER) AS note_premiere_commande,
    COUNT(*) AS clients,
    SUM(co.nb_commandes > 1) AS clients_recurrents,
    ROUND(SUM(co.nb_commandes > 1) * 100.0 / COUNT(*), 2) AS taux_reachat
FROM commandes_ordonnees co
JOIN note_par_commande n ON n.order_id = co.order_id
WHERE co.rang = 1
GROUP BY note_premiere_commande
ORDER BY note_premiere_commande;
