-- 6. Top 10 des catégories par chiffre d'affaires produit
-- Le CA est ici la somme des prix des articles (hors frais de port), car le
-- paiement n'est pas ventilé par article.
WITH ventes AS (
    SELECT
        COALESCE(t.product_category_name_english, pr.product_category_name, 'non_renseignee') AS categorie,
        i.order_id,
        i.price
    FROM order_items i
    JOIN orders o ON o.order_id = i.order_id
    JOIN products pr ON pr.product_id = i.product_id
    LEFT JOIN category_translation t ON t.product_category_name = pr.product_category_name
    WHERE o.order_status = 'delivered'
)
SELECT
    categorie,
    COUNT(DISTINCT order_id) AS commandes,
    COUNT(*) AS articles_vendus,
    ROUND(SUM(price), 2) AS ca_produits,
    ROUND(SUM(price) * 100.0 / (SELECT SUM(price) FROM ventes), 2) AS part_ca,
    ROUND(AVG(price), 2) AS prix_moyen_article
FROM ventes
GROUP BY categorie
ORDER BY ca_produits DESC
LIMIT 10;
