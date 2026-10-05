# ADR 0002 : SQLite plutôt qu'un fichier JSON ou un serveur PostgreSQL

- Statut : proposé
- Date : 2026-10-05
- Décideurs : smarjane et titiThibaud1

## Contexte
L’association utilise Biblio pour gérer les prêts de livres entre bénévoles.  
Nous avons besoin d’un stockage simple, fiable, et utilisable par tous les bénévoles, même ceux qui n’ont pas de compétences techniques ou d’installation complexe sur leur machine.

## Options envisagées
### 1. Fichier JSON
**Pour :** très simple, aucun logiciel à installer.  
**Contre :** facilement corrompu, pas adapté à plusieurs accès, pas de vraies requêtes.

### 2. SQLite
**Pour :** base SQL complète, stable, fonctionne dans un simple fichier, aucune installation.  
**Contre :** nécessite un minimum de SQL.

### 3. Serveur PostgreSQL
**Pour :** très robuste, professionnel.  
**Contre :** installation lourde, nécessite un serveur, trop complexe pour des bénévoles.

## Décision
Nous proposons d’utiliser SQLite comme solution de stockage pour Biblio.

## Conséquences
### Plus facile
- Tester le projet sur n’importe quel ordinateur des bénévoles.  
- Utiliser des requêtes SQL simples pour gérer les livres.  
- Aucune installation de serveur.

### Plus difficile
- Nécessite d’apprendre un peu de SQL.  
