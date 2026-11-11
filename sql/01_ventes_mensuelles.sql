-- 1. Ventes mensuelles : commandes, chiffre d'affaires et panier moyen
-- Les paiements sont d'abord agrégés par commande : une commande peut avoir
-- plusieurs lignes de paiement (carte + bon d'achat), donc AVG(payment_value)
-- sous-estimerait le panier moyen.
-- Période : janvier 2017 à août 2018 (les mois antérieurs et postérieurs sont incomplets).
WITH paiement_par_commande AS (
    SELECT order_id, SUM(payment_value) AS montant
    FROM payments
    GROUP BY order_id
)
SELECT
    STRFTIME('%Y-%m', o.order_purchase_timestamp) AS mois,
    COUNT(*) AS total_commandes,
    ROUND(SUM(p.montant), 2) AS chiffre_affaires,
    ROUND(AVG(p.montant), 2) AS panier_moyen
FROM orders o
JOIN paiement_par_commande p ON p.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.order_purchase_timestamp >= '2017-01-01'
  AND o.order_purchase_timestamp < '2018-09-01'
GROUP BY mois
ORDER BY mois;
