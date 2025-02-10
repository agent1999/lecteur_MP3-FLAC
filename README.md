# Lecteur MP3 et FLAC

Un logiciel en Python lisant des playlists XSPF de fichiers MP3 et FLAC et leurs méta-données. Le lecteur permet de :
- écouter les fichiers MP3 et FLAC
- lire leurs méta-données et les modifier
- créer des playlists XSPF de fichiers MP3 et FLAC et les modifier
- rechercher les informations d'albums via l'API Deezer
  
Le lecteur est utilisable en mode console et en mode graphique.

## Comment installer

### Pré-requis

- Python 3.0 ou supérieur.
- Bibliothèques nécessaires à installer à l'aide de la commande `pip` dans le `Terminal` : 

  ```
  pip install tinytag
  pip install playsound
  pip install python-magic
  pip install music-tag
  pip install pygame
  pip install requests
  ```

### Mode Console
- Ouvrir une fenêtre du `Terminal`.
- Aller dans le dossier src à l'aide de la commande `cd`.
- Il existe 4 modes de fonctionnement du lecteur, le mode de fonctionnement se choisit au moment d'écrire la ligne de commande :
  - `-f` : Afficher les méta-données d'un fichier MP3 ou FLAC.
    ```
    python3 cli.py -f [FICHIER]
    ```

    Après l'affichage des méta-données, le lecteur propose d'écouter le fichier. Taper `O` pour écouter ou `N` pour terminer.

  - `-d` : Afficher les fichiers MP3 et FLAC présents dans l'arborescence d'un dossier.
    ```
    python3 cli.py -d [DOSSIER]
    ```

  - `-o` : Sauvegarder une playlist XSPF des fichiers MP3 et FLAC présents dans l'arborescence d'un dossier, utilisable seulement avec -d.
    ```
    python3 cli.py -d [DOSSIER] -o [PLAYLIST]
    ```

  - `-h` ou `--help` : Afficher le manuel.
    ```
    python3 cli.py -h
    ```
  
### Mode GUI

- Ouvrir une fenêtre du `Terminal`.
- Aller dans le dossier src à l'aide de la commande `cd`.
- Pour lancer le lecteur, taper :

  ```
  python3 gui.py
  ```

## Journal des modifications

### Version 1.1

- Déplacement du dossier images depuis le dossier library vers le dossier src.
- Mise à jour des chemins des fichiers du dossier images dans gui.py.
- Suppression du dossier library.

### Version 1.0

- Sortie initiale.

## Crédits

- Merci à [Goboun](https://github.com/Goboun) et S pour avoir travaillé avec moi sur le lecteur.
