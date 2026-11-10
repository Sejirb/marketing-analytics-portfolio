# 📊 E-Commerce SQL Analytics & Customer Retention

Étude approfondie de performance commerciale et d'analyse comportementale client basée sur le dataset public **Olist** (~100 000 commandes réelles).

## 🎯 Problématique Business
Identifier les leviers de croissance du chiffre d'affaires et évaluer l'efficacité des efforts d'acquisition face à la rétention client.

## 🔍 Principaux Résultats & Insights
1. **Saisonnalité & Chiffre d'Affaires :** 
   - Forte croissance continue des volumes de vente sur 2017-2018, avec un pic majeur d'activité en novembre (Black Friday).
   - Panier moyen stable oscillant autour de 160 R$.
2. **Fuite dans le modèle de fidélisation (Rétention critique) :**
   - **~97 % des clients n'ont passé qu'une seule commande** sur la marketplace.
   - Moins de 3 % des acheteurs sont récurrents.
3. **Recommandations Stratégiques :**
   - Réorienter une part du budget d'acquisition payante (Paid Ads) vers des leviers d'activation et de fidélisation CRM (séquences d'onboarding e-mail, offres de réachat à J+30).
   - Mettre en place un programme VIP pour les clients multi-acheteurs à forte LTV (Customer Lifetime Value).

## 🛠️ Stack Technique
- **SQL (SQLite)** : Jointures multi-tables (`JOIN`), Common Table Expressions (`WITH`), fonctions d'agrégation (`COUNT DISTINCT`, `SUM`, `AVG`), manipulation temporelle (`STRFTIME`).
- **Python (Pandas)** : Ingestion des données brutes et automatisation de l'exécution des requêtes.

## 📂 Structure du Répertoire
- `setup_db.py` : Script d'ingestion et création de la base relationnelle SQLite.
- `run_query.py` : Script d'exécution des requêtes analytiques avec restitution tabulaire.
- `sql/business_queries.sql` : Ensemble des requêtes documentées et commentées.