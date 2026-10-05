## Biblio

Le projet est une bibliothèque qui permet d'emprunter des livres et suivre leurs états d'emprunt. Ils concernent les étudiants.


## Prérequis

Sous macOS ou Linux : python3.
Sous Windows, si python ne marche pas : py.


## Installation

1. Cloner le dépôt avec GitHub Desktop.
2. Ouvrir un terminal dans le dossier.
3. Créer la base de démonstration :

```python biblio.py init```
   Résultat attendu :
   Base initialisee : 6 livres, 3 membres.

## Utilisation

```python biblio.py init```
Remet les données de départ


```python biblio.py livres```
Liste les livres, disponibles ou empruntés


```python biblio.py chercher <texte>```
Cherche un titre

```python biblio.py emprunter <livre> <membre>```
Enregistre un emprunt


```python biblio.py rendre <livre>```
Enregistre un retour

```python biblio.py retards```
Liste les livres non rendus depuis plus de 14 jours


## Tests


## Structure du projet


## Contribuer

1. Ouvrez une issue, ou choisissez-en une.
2. Créez une branche : fix/<numero>-<problème>
3. Commitez : fix: <description du problème>
4. Ouvrez une Pull Request avec « Closes #<numero> ».
5. Attendez une review avant de merger.



## Auteurs

Réalisé par :
- SELMANE Marjane
- SELLIER Thibaud

