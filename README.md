# Gestion de Base de Données

## Description
Cette application en Python utilise Tkinter pour créer une interface graphique permettant la gestion d'une base de données SQLite. Elle vous permet de parcourir un dossier, d'ajouter des fichiers à la base de données, de trier et de supprimer.

## Contexte
Cette application est réaliser dans le cadre d'un devoir universitaire visant à apprendre les base d'un programme de création et de gestion d'une base de données.

## Fonctionnalités
- Parcourir un dossier et ses sous dossier pour ajouter des fichiers à la base de données.
- Afficher les fichiers dans une interface graphique avec la possibilité de trier par différents critères.
- Supprimer des fichiers de la base de données.
- Faire des recherche par filtre ou par nom

## Utilisation
1. Ouvrir l'application (avec l'éxécutable ou en ligne de commande voir fin de page).
2. Utiliser le menu "Fichier" pour parcourir un dossier ou quitter l'application.
4. Cliqué un première fois sur le "rechercher par nom" pour afficher la base de Données
3. Utiliser les boutons pour trier, supprimer, ou rechercher des fichiers par nom comme suit dans la documentation.

## Base de données
Une base de données a été intégrée pour stocker des informations sur les fichiers, telles que :
1. L’ID dans la base de données (son index). 2. Le nom du fichier.
3. Le chemin d’accès au fichier.
4. La date d’ajout.
5. La date de modification. 6. Le type (extensions).
7. La taille.
Elle est créée automatiquement si aucune n’est donnée en paramètre.

## Aide
Une section aide est disponible dans le menu. Elle ouvre un document text (Ou un lien vers mon GitHub) pour vous aider. Elle contient de plus amples informations.  

## Prérequis
- Python 3.x
- Tkinter (inclus dans la plupart des installations Python)
- SQLite3 (inclus dans la plupart des installations Python)

## Installation
1. Cloner le référentiel : `git clone https://github.com/Nawfoel-Ardjoune/BDD_web`
2. Accéder au répertoire du projet : `cd votre-repo`
3. Installer les dépendances : `pip install -r requirements.txt` (si nécessaire)

## Lancement de l'application
Executable: BDD_prog.exe
		ou
```bash
python BDD_prog.py
