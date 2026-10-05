# ADR 0003 : Requêtes paramétrées

- Statut : proposé
- Date : 2026-10-05
- Décideurs : smarjane et titiThibaud1


## Contexte

L’application Biblio permet aux bénévoles de consulter, ajouter et modifier des informations concernant les livres et les emprunts.

Certaines fonctionnalités nécessitent d’effectuer des recherches dans la base de données à partir de valeurs saisies par les utilisateurs. Construire les requêtes SQL en concaténant directement ces valeurs peut entraîner des erreurs ou des failles de sécurité, notamment des injections SQL.

Nous devons choisir une méthode pour exécuter les requêtes SQL de manière fiable et sécurisée.


## Options envisagées

### 1. Concaténation de chaînes SQL

**Pour :** simple à écrire et à comprendre.

**Contre :** risque élevé d’injection SQL, gestion compliquée des caractères spéciaux, maintenance plus difficile.

### 2. Requêtes paramétrées

**Pour :** protège contre les injections SQL, améliore la lisibilité du code, facilite la maintenance et la réutilisation des requêtes.

**Contre :** nécessite de comprendre le principe des paramètres SQL.


## Décision

Nous proposons d’utiliser systématiquement des requêtes paramétrées pour tous les accès à la base de données SQLite de Biblio.

Les valeurs fournies par les utilisateurs seront transmises sous forme de paramètres plutôt que d’être directement insérées dans les chaînes SQL.


## Conséquences

### Plus facile

- Sécuriser l’application contre les injections SQL.
- Gérer correctement les caractères spéciaux présents dans les données.
- Maintenir et relire les requêtes SQL.
- Réutiliser les mêmes requêtes avec des valeurs différentes.

### Plus difficile

- Demande de maîtriser la syntaxe des requêtes paramétrées.
- Nécessite davantage de rigueur lors du développement des accès aux données.
