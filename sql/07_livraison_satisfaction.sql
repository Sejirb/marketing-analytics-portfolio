-- 7. Impact du retard de livraison sur la note client
-- Retard = date de livraison réelle comparée à la date estimée annoncée au client.
-- Une commande peut avoir plusieurs avis : on en fait la moyenne par commande.
WITH note_par_commande AS (
    SELECT order_id, AVG(review_score) AS note
    FROM reviews
    GROUP BY order_id
),
livraisons AS (
    SELECT
        JULIANDAY(o.order_delivered_customer_date)
            - JULIANDAY(o.order_estimated_delivery_date) AS jours_retard,
        n.note
    FROM orders o
    JOIN note_par_commande n ON n.order_id = o.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
),
tranches AS (
    SELECT
        CASE
            WHEN jours_retard <= 0 THEN 1
            WHEN jours_retard <= 3 THEN 2
            WHEN jours_retard <= 7 THEN 3
            ELSE 4
        END AS ordre,
        CASE
            WHEN jours_retard <= 0 THEN 'À l''heure ou en avance'
            WHEN jours_retard <= 3 THEN 'Retard de 3 jours ou moins'
            WHEN jours_retard <= 7 THEN 'Retard de 3 à 7 jours'
            ELSE 'Retard de plus de 7 jours'
        END AS livraison,
        note
    FROM livraisons
)
SELECT
    livraison,
    COUNT(*) AS commandes,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM livraisons), 1) AS part_commandes,
    ROUND(AVG(note), 2) AS note_moyenne,
    ROUND(SUM(note <= 2) * 100.0 / COUNT(*), 1) AS part_notes_negatives
FROM tranches
GROUP BY ordre, livraison
ORDER BY ordre;
