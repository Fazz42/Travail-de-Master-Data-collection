# Travail de Master - Collecte de Données

Ce projet est le résultat d'un Mémoire de Master. Il vise à analyser les différences de qualité de diverses méthodes de recherche dans les bases de données médicales, incluant la recherche par code ICD-10, la recherche textuelle simple, la recherche textuelle multiple, et la recherche par requêtes SNOMED CT.

## Structure du Projet

- **Snomed_precision.py, precision_icd.py, precision_multi.py, precision_single.py**: Scripts pour évaluer la précision des résultats.
- **count.py, count2.py**: Scripts pour le décompte des occurrences.
- **graphs.py**: Script pour la génération de graphiques et l'analyse statistique comparée à ICD-10.
- **script_complet.py**: Script principal générant les résultats des différentes méthodes.
- **données**: Le dossier `results` contient les résultats des analyses effectuées.

## Installation

Pour exécuter les scripts, vous aurez besoin de Python 3, d'un serveur web Snowstorm, des fichiers Excel contenant les données, ainsi que des dépendances listées dans `requirements.txt`. Vous pouvez installer ces dernières avec la commande :

```bash
pip install -r requirements.txt

````

## Utilisation

Chaque script peut être exécuté individuellement pour analyser des aspects spécifiques des données. Les résultats sont stockés dans le dossier `results`.

## Auteurs

- François Marchal
