# Objectifs:
  Ce projet met en œuvre les capacités de l'étudiant à mettre en place une extraction de données depuis Internet. La gestion de type "Extract-Transform-Load" sera donc une finalité
  La mise en œuvre de la bibliothèque d'analyse syntaxique HTML BeautifulSoup4 sera également une première approche de la gestion des bibliothèques

__1. Extraction données depuis BooKToScrape__
  *(Cours apprentissage Python OpenClassrooms)*

Le code python de ce projet, permet de composer un inventaire des livres contenus dans la bibliothèque BookToScrape.com.
Le résultat de ce programme est l'enregistrement local d'une arborescence de dossiers/fichiers, suivant les thèmes référencés dans le site.
Chaque dossier par thème inclut :

1. Un dossier images par thème stockant la couverture de chaque livre.
2. un fichier .csv comportant les principales caractéristiques de chaque livre du thème, complète chaque dossier.

__2. Déploiement du projet.__

Dans un environnement Python 3.11.3 virtuel et actif 

- Décompresser le fichier *.zip* à la racine du dossier et lancer depuis la console Bash :
**pip install -r requirements.txt**
Les paquets nécessaires sont alors déployés sur l'environnement virtuel.
    Depuis la console Bash dans l'environnement virtuel activé, lancer le script du projet par la commande:
    **_python.exe books_to_scrape.py_**
