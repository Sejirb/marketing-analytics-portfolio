-- 5. Valeur client selon la fréquence d'achat
-- Combien rapporte un client récurrent par rapport à un client à commande unique,
-- et quel poids pèsent les récurrents dans le chiffre d'affaires ?
WITH paiement_par_commande AS (
    SELECT order_id, SUM(payment_value) AS montant
    FROM payments
    GROUP BY order_id
),
valeur_client AS (
    SELECT
        c.customer_unique_id,
        COUNT(*) AS nb_commandes,
        SUM(p.montant) AS ca_client
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    JOIN paiement_par_commande p ON p.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT
    CASE
        WHEN nb_commandes = 1 THEN '1 commande'
        WHEN nb_commandes = 2 THEN '2 commandes'
        ELSE '3 commandes et plus'
    END AS segment,
    COUNT(*) AS clients,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM valeur_client), 2) AS part_clients,
    ROUND(AVG(ca_client), 2) AS ca_moyen_par_client,
    ROUND(SUM(ca_client) / SUM(nb_commandes), 2) AS panier_moyen,
    ROUND(SUM(ca_client) * 100.0 / (SELECT SUM(ca_client) FROM valeur_client), 2) AS part_ca
FROM valeur_client
GROUP BY segment
ORDER BY segment;
