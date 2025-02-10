#!/usr/bin/python3
# −*− coding: UTF−8 −*−

#Bibliothèque pour les paramètres de la ligne de commande
import sys

#Bibliothèque pour l'exploration d'une arborescence
import os

#Bibliothèque pour l'extraction de méta-données
#Taper dans le terminal "pip install tinytag" pour installer la bibliothèque
from tinytag import TinyTag

#Bilbiothèque cross-plateforme pour écouter un son
#Taper dans le terminal "pip install playsound" pour installer la bibliothèque
from playsound import playsound

#Bibliothèque pour vérifier le type MIME des fichiers
import magic
mime = magic.Magic(mime=True)

def cli():
    """!
    @brief Mode console du logiciel, en fonction du nombre de paramètres, on vérifie que la ligne de commande est correcte, puis on la traite la commande saisie 
    """
    argv = sys.argv
    if len(argv) == 2: #Aide
        if argv[1].__eq__("-h") or argv[1].__eq__("--help"):
            help()
        else:
            rerror()
    elif len(argv) == 3: #Sans fichier de sortie
        if argv[1].__eq__("-d"): #Dossier
            affiche_arborescence(argv[2], "nul", 0)
        elif argv[1].__eq__("-f"): #Fichier
            affiche_metadonnees(argv[2])
        else:
            rerror()
    elif len(argv) == 5: #Avec fichier de sortie
        if argv[1].__eq__("-d") and argv[3].__eq__("-o"): #Dossier
            affiche_arborescence(argv[2], argv[4], 1)
        else: 
            rerror()
    else: #Aucun ou trop de paramètres
        rerror()

def help():
    """!
    @brief Manuel utilisateur du logiciel en mode console
    """
    print("Utilisation :")
    print("  -f <fichier> : analyser un fichier MP3 ou FLAC")
    print("  -d <dossier> : explorer un dossier pour générer une playlist")
    print("  -d <dossier> -o <fichier> : sauvegarder la playlist dans un fichier XSPF")
    print("  -h, --help : afficher l'aide")
    print("Quelques scénarios d’exécution : ")
    print("\tpython3 cli.py")
    print("\tpython3 cli.py -h")
    print("\tpython3 cli.py -d .")
    print("\tpython3 cli.py -f music.mp3")
    print("\tpython3 cli.py -d ./music/ -o playlist.xspf")
    
def rerror():
    """!
    @brief Message d'erreur fonctionnelle quand il y a aucun paramètre, trop de paramètres, ou pas les bons paramètres 
    """
    print("Mauvais paramètre(s) : taper « -h » ou « --help » pour obtenir de l'aide")

def serror():
    """!
    @brief Message d'erreur fonctionnelle quand le fichier n'est pas un fichier MP3/FLAC
    """
    print("Erreur : le fichier n'est un MP3/FLAC")
        
def affiche_arborescence(dossier:str, xspf:str, avecXSPF:bool):
    """!
    @brief Affiche les MP3 et les FLAC dans une arborescene en entrée, et les sauvegarde dans un fichier en entrée
    @param dossier le chemin du dossier à explorer
    @param xspf le chemin du fichier XSPF dans lequel la playlist sera sauvegardée
    @param avecXSPF pour indiquer si on va enregistrer la playlist
    """
    if avecXSPF:
        with open(xspf, 'w') as fichier_xspf:
            fichier_xspf.write('<?xml version="1.1" encoding="UTF-8"?>\n')
            fichier_xspf.write('<playlist version="1" xmlns="http://xspf.org/ns/0/">\n')
            fichier_xspf.write('  <trackList>\n')
            for chemin, dossiers, fichiers in os.walk(dossier):
                for f in fichiers:
                    #Vérification de l'extension
                    if f.lower().endswith(".mp3") or f.lower().endswith(".flac"):
                        #Vérification du type MIME
                        type = mime.from_file(os.path.join(chemin, f))
                        if(type == "audio/mpeg" or type == "audio/flac" or  type == "audio/x-flac"):
                            fichier_xspf.write('    <track>\n')
                            fichier_xspf.write(f'      <location>{os.path.abspath(os.path.join(chemin, f))}</location>\n') # mettre file://
                            fichier_xspf.write(f'      <title>{f}</title>\n')
                            fichier_xspf.write('    </track>\n')
            fichier_xspf.write('  </trackList>\n')
            fichier_xspf.write('</playlist>\n')
    else:
        for chemin, dossiers, fichiers in os.walk(dossier):
            for f in fichiers:
                if f.lower().endswith(".mp3") or f.lower().endswith(".flac"):
                    print(f) #print(os.path.join(chemin, f)) pour le chemin relatif

def affiche_metadonnees(fichier:str):
    """!
    @brief Affiche les métadonnées d'un MP3 ou d'un FLAC en entrée
    @param fichier le chemin de la musique à extraire
    """
    #Vérification de l'extension
    if fichier.lower().endswith(('.mp3', '.flac')):
        #Vérification du type MIME
        type = mime.from_file(fichier)
        if(type == "audio/mpeg" or type == "audio/flac" or type == "audio/x-flac"):
            musique = TinyTag.get(fichier)
            print(f"Titre : {musique.title}")
            print(f"Artiste : {musique.artist}")
            print(f"Album : {musique.album}")
            print(f"Artiste de l'album : {musique.albumartist}")
            print(f"Compositeur : {musique.composer}")
            print(f"Genre : {musique.genre}")
            print(f"Année : {musique.year}")
            print(f"Piste : {musique.track} sur {musique.track_total}")
            print(f"Numéro de disque : {musique.disc} sur {musique.disc_total}")
            print(f"BPM : {musique.other.get('bpm')}")
            print(f"Commentaire : {musique.comment}")
            print(f"Souhaitez-vous écouter {musique.title} ? (O/N)")
            reponse = input()
            if(reponse == "O"):
                playsound(fichier)
        else:
            serror()
    else:
        serror()

#Programmme principal
cli()