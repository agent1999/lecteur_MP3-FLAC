#!/usr/bin/python3
# −*− coding: UTF−8 −*−

#Bibliothèque pour l'interface graphique
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage

#Bibliothèque pour l'exploration des dossiers et les chemins
import os

#Bibliothèque pour vérifier le type MIME des fichiers
import magic
mime = magic.Magic(mime=True)

#Bibliothèque pour la lecture et la modification des méta-données des musiques
#Taper dans le terminal "pip install music-tag" pour installer la bibliothèque
import music_tag

#Bibliothèque pour récuperer les covers d'albums et de musiques, ainsi que les icones utilisés
from PIL import Image, ImageTk

#Bibliothèque pour la lecture des musiques
#Taper dans le terminal "pip install pygame" pour installer la bibliothèque
import pygame

#Bibliothèque pour récupérer les informations de l'API
import requests

#Programme principal
#Initialisation du menu principal
root = tk.Tk()
root.title("Lecteur MP3/FLAC")
root.geometry("600x300")
root.configure(bg="white")
root.resizable(False, False)

#Icones pour rendre jolie l'interface
iconButton1 = PhotoImage(file="images/icon-metadata.png")
iconButton2 = PhotoImage(file="images/dossier.png")
iconButton3 = PhotoImage(file="images/playlist.png")
iconButton4 = PhotoImage(file="images/loupe.png")
iconExport = PhotoImage(file="images/icon-export.png")

#Zone pour mettre le label du menu principal et l'icône de la note de musique côte à côte (pack)
welcome_frame = tk.Frame(root, bg="white")
welcome_frame.pack(pady=20)

#Icone Note de musique pour le label du menu principal
photo = PhotoImage(file="images/music_note.png")
photo_label = tk.Label(welcome_frame, image=photo, bg="white")
photo_label.image = photo
photo_label.pack(side="right", padx=5)

#Label Menu principal
welcome_label = tk.Label(welcome_frame, text="Menu Principal", font=("Poppins", 16, "bold"), bg="white", fg="black")
welcome_label.pack(side="right", padx=5)

#La suite du menu principal se trouve tout en bas du fichier

#Fenêtre Afficher méta-données d'un fichier à sélectionner
def select_file():
    """!
    @brief Sélectionner un fichier audio et afficher ses métadonnées
    """
    #Sélection du fichier et vérification de l'extension
    file_path = filedialog.askopenfilename(title="Sélectionner un fichier audio", filetypes=[("Audio Files", "*.mp3 *.flac")])
    if not file_path:
        messagebox.showwarning("Avertissement", "Aucun fichier sélectionné")
    else:
        #Vérification du type MIME
        mime = magic.Magic(mime=True)
        type = mime.from_file(file_path)
        
        if(type == "audio/mpeg" or type == "audio/flac" or type == "audio/x-flac"):
            #Initialisation de la fenêtre des méta-données
            metadata_window = tk.Toplevel(root, bg = "white")
            metadata_window.title(os.path.basename(file_path))
            metadata_window.geometry("1000x500")
            #Pour que les widgets s'affichent en fonction de la taille de la cover quelle que soit sa forme
            metadata_window.grid_columnconfigure(0, weight=1)
            metadata_window.grid_columnconfigure(2, weight=1)
            metadata_window.grid_rowconfigure(0, weight=1)
            metadata_window.grid_rowconfigure(1, weight=1)
            metadata_window.grid_rowconfigure(2, weight=1)
            metadata_window.grid_rowconfigure(3, weight=1)
            metadata_window.grid_rowconfigure(4, weight=1)
            metadata_window.grid_rowconfigure(5, weight=1)
            metadata_window.grid_rowconfigure(6, weight=1)
            metadata_window.grid_rowconfigure(7, weight=1)
            metadata_window.grid_rowconfigure(8, weight=1)
            metadata_window.grid_rowconfigure(9, weight=1)
            metadata_window.grid_rowconfigure(10, weight=1)

            #Méta-données de la musique
            musique = music_tag.load_file(file_path)
            song_name = musique.raw["tracktitle"]
            artist_name = musique.raw["artist"]
            album_name = musique.raw["album"]
            album_artiste_name = musique.raw["albumartist"]
            compositor = musique.raw["composer"]
            genre = musique.raw["genre"]
            year = musique.raw["year"]
            track_number = musique.raw["tracknumber"]
            track_number_total = musique.raw["totaltracks"]
            disc_number = musique.raw["discnumber"]
            disc_number_total = musique.raw["totaldiscs"]
            comment = musique.raw["comment"]

            #Zone Cover + bouton Ecoute
            frame_cover_play = tk.Frame(metadata_window, bg="white")
            frame_cover_play.grid(row = 0, column = 0, pady=20, rowspan=11)

            #Label Cover de la musique
            '''S'il y a une cover on l'affiche, sinon on affiche un placeholder'''
            if hasattr(musique["artwork"].first, "data"):
                image_donnee = musique["artwork"].first.data
                with open("images/cover.jpeg", "wb") as f:
                    f.write(image_donnee)
                image = Image.open("images/cover.jpeg")
            else:
                image = Image.open("images/sans_cover.jpeg")
            '''Pour conserver le ratio dans le cas où les covers ne sont pas carrés'''
            image.thumbnail((300, 300))
            cover_image = ImageTk.PhotoImage(image)
            cover_label = tk.Label(frame_cover_play, image=cover_image)
            cover_label.image = cover_image
            cover_label.grid(row = 0, column = 0, pady=(0,20))

            #Bouton Ecoute de la musique
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            image = Image.open("images/play.jpeg")
            image.thumbnail((50, 50))
            play_image = ImageTk.PhotoImage(image)
            image = Image.open("images/stop.jpeg")
            image.thumbnail((50, 50))
            stop_image = ImageTk.PhotoImage(image)
            def play():
                """!
                @brief Lancer l'écoute de la musique, en lien ave le bouton Ecoute
                """
                pygame.mixer.music.play()
                file_player_button.configure(image=stop_image, command=pause)
                file_player_button.config(bg='white', activebackground='white', highlightthickness=0, bd=0, border=0)
            def pause():
                """!
                @brief Mettre en pause l'écoute la musique
                """
                pygame.mixer.music.pause()
                file_player_button.configure(image=play_image, command=continu)
                file_player_button.config(bg='white', activebackground='white', highlightthickness=0, bd=0, border=0)
            def continu():
                """!
                @brief Reprendre l'écoute de la musique
                """
                pygame.mixer.music.unpause()
                file_player_button.configure(image=stop_image, command=pause)
            file_player_button = tk.Button(frame_cover_play, bg="white", highlightbackground="white", image=play_image, command=play)
            file_player_button.grid(row=1, column=0, pady=(20,0))
            '''Pour que la musique s'arrête quand on quitte la fenêtre, sinon elle continue en arrière-plan...'''
            def on_closing():
                """!
                @brief Arrêter la musique quand la fenêtre se ferme
                """
                pygame.mixer.music.stop()
                metadata_window.destroy()
            metadata_window.protocol("WM_DELETE_WINDOW", on_closing)

            #Affichage des méta-données dans la fenêtre
            #Titre
            label_titre = tk.Label(metadata_window, text=f"Titre : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
            label_titre.grid(row=0, column=1, pady= 5, sticky = 'E')
            text_titre = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
            text_titre.grid(row=0, column=2, pady= 5, sticky = 'W')
            if song_name:
                text_titre.insert("1.0", song_name)

            #Artiste
            label_artiste = tk.Label(metadata_window, text=f"Artiste : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
            label_artiste.grid(row=1, column=1, pady= 5, sticky = 'E')
            text_artiste = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
            text_artiste.grid(row=1, column=2, pady= 5, sticky = 'W')
            if artist_name:
                text_artiste.insert("1.0", artist_name)

            #Album
            label_album = tk.Label(metadata_window, text=f"Album : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
            label_album.grid(row=2, column=1, pady= 5, sticky = 'E')
            text_album = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
            text_album.grid(row=2, column=2, pady= 5, sticky = 'W')
            if album_name:
                text_album.insert("1.0", album_name)

            #Artiste de l'album
            label_artiste_album = tk.Label(metadata_window, text=f"Artiste de l'album : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
            label_artiste_album.grid(row=3, column=1, pady= 5, sticky = 'E')
            text_artiste_album = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
            text_artiste_album.grid(row=3, column=2, pady= 5, sticky = 'W')
            if album_artiste_name:
                text_artiste_album.insert("1.0", album_artiste_name)

            #Compositeur
            label_compositeur = tk.Label(metadata_window, text=f"Compositeur : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
            label_compositeur.grid(row=4, column=1, pady= 5, sticky = 'E')
            text_compositeur = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
            text_compositeur.grid(row=4, column=2, pady= 5, sticky = 'W')
            if compositor:
                text_compositeur.insert("1.0", compositor)

            #Genre
            label_genre = tk.Label(metadata_window, text=f"Genre : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
            label_genre.grid(row=5, column=1, pady= 5, sticky = 'E')
            text_genre = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
            text_genre.grid(row=5, column=2, pady= 5, sticky = 'W')
            if genre:
                text_genre.insert("1.0", genre)

            #Année
            label_annee = tk.Label(metadata_window, text=f"Année :", bg= "white", fg="black", font=("Poppins", 14, "bold"))
            label_annee.grid(row=6, column=1, pady= 4, sticky = 'E')
            text_annee = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
            text_annee.grid(row=6, column=2, pady= 5, sticky = 'W')
            if year:
                text_annee.insert("1.0", year)

            #Piste
            label_piste = tk.Label(metadata_window, text=f"Piste : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
            label_piste.grid(row=7, column=1, pady= 5, sticky = 'E')
            frame_piste = tk.Frame(metadata_window, bg="white")
            frame_piste.grid(row=7, column=2, pady= 5, sticky = 'W')
            text_piste = tk.Text(frame_piste, width= 2, height=1, bg="white", fg="black", font=("Poppins", 14))
            text_piste.grid(row=0, column=0, pady= 5, sticky = 'W')
            label_sur_piste = tk.Label(frame_piste, text=" sur ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
            label_sur_piste.grid(row=0, column=1, pady= 5, sticky = 'W')
            text_piste_total = tk.Text(frame_piste, width= 2, height=1, bg="white", fg="black", font=("Poppins", 14))
            text_piste_total.grid(row=0, column=2, pady= 5, sticky = 'W')
            if track_number:
                text_piste.insert("1.0", track_number)
            if track_number_total:
                text_piste_total.insert("1.0", track_number_total)

            #Numéro de disque
            label_numero_disque = tk.Label(metadata_window, text=f"Numéro de disque : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
            label_numero_disque.grid(row=8, column=1, pady= 5, sticky = 'E')
            frame_numero_disque = tk.Frame(metadata_window, bg="white")
            frame_numero_disque.grid(row=8, column=2, pady= 5, sticky = 'W')
            text_numero_disque = tk.Text(frame_numero_disque, width= 2, height=1, bg="white", fg="black", font=("Poppins", 14))
            text_numero_disque.grid(row=0, column=0, pady= 5, sticky = 'W')
            label_sur_numero_disque = tk.Label(frame_numero_disque, text=" sur ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
            label_sur_numero_disque.grid(row=0, column=1, pady= 5, sticky = 'W')
            text_numero_disque_total = tk.Text(frame_numero_disque, width= 2, height=1, bg="white", fg="black", font=("Poppins", 14))
            text_numero_disque_total.grid(row=0, column=2, pady= 5, sticky = 'W')
            if disc_number:
                text_numero_disque.insert("1.0", disc_number)
            if disc_number_total:
                text_numero_disque_total.insert("1.0", disc_number_total)

            #Commentaire
            label_comment = tk.Label(metadata_window, text=f"Commentaire : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
            label_comment.grid(row=9, column=1, pady= 5, sticky = 'E')
            text_comment = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
            text_comment.grid(row=9, column=2, pady= 5, sticky = 'W')
            if comment:
                text_comment.insert("1.0", comment)

            #Enregistrer les méta-données
            def enregistrer_meta_donnees():
                """!
                @brief Commande du bouton Enregistrer : 
                Enregistrer les méta-données du fichier 
                en récupérant le contenu des champs de textes des méta-données
                """
                musique.raw["tracktitle"] = text_titre.get("1.0", "end")
                musique.raw["artist"] = text_artiste.get("1.0", "end")
                musique.raw["album"] = text_album.get("1.0", "end")
                musique.raw["albumartist"] = text_artiste_album.get("1.0", "end")
                musique.raw["composer"] = text_compositeur.get("1.0", "end")
                musique.raw["genre"] = text_genre.get("1.0", "end")
                musique.raw["year"] = text_annee.get("1.0", "end")
                musique.raw["tracknumber"] = text_piste.get("1.0", "end")
                musique.raw["totaltracks"] = text_piste_total.get("1.0", "end")
                musique.raw["discnumber"] = text_numero_disque.get("1.0", "end")
                musique.raw["totaldiscs"] = text_numero_disque_total.get("1.0", "end")
                musique.raw["comment"] = text_comment.get("1.0", "end")
                musique.save()
                messagebox.showinfo("Succès", "Opération d'enregistrement faite avec succès")

            #Bouton Enregistrer les méta-données
            button_enregistrer = tk.Button(metadata_window, fg="black", highlightbackground="white", compound="right", padx=10, pady=5,text="Enregistrer", command=enregistrer_meta_donnees)
            button_enregistrer.grid(row=10, column=2, padx=5, pady=5, sticky="W")

        #Si le fichier séléctionné n'est pas un fichier mp3/FLAC MIME, un message apparait
        else:
            messagebox.showwarning("Avertissement", "Le fichier sélectionné n'est pas un MP3/FLAC")
            
#Fenêtre Afficher méta-données d'un fichier quand on clique sur l'un des boutons des fichiers dans la fenêtre d'exportation/d'importation
#Pré-condition : l'extension de audio_file est mp3/FLAC et de type audio/mpeg ou audio/flac
def select_file2(audio_file:str):
    """!
    @brief Afficher les métadonnées d'un fichier audio en entrée
    @param audio_file le chemin absolu du fichier audio
    """
    file_path = audio_file
    if not file_path:
        messagebox.showwarning("Avertissement", "Le fichier n'existe plus")
    else:
        #Initialisation de la fenêtre des méta-données
        metadata_window = tk.Toplevel(root, bg = "white")
        metadata_window.title(os.path.basename(file_path))
        metadata_window.geometry("1000x500")
        #Pour que les widgets s'affichent en fonction de la taille de la cover quelle que soit sa forme
        metadata_window.grid_columnconfigure(0, weight=1)
        metadata_window.grid_columnconfigure(2, weight=1)
        metadata_window.grid_rowconfigure(0, weight=1)
        metadata_window.grid_rowconfigure(1, weight=1)
        metadata_window.grid_rowconfigure(2, weight=1)
        metadata_window.grid_rowconfigure(3, weight=1)
        metadata_window.grid_rowconfigure(4, weight=1)
        metadata_window.grid_rowconfigure(5, weight=1)
        metadata_window.grid_rowconfigure(6, weight=1)
        metadata_window.grid_rowconfigure(7, weight=1)
        metadata_window.grid_rowconfigure(8, weight=1)
        metadata_window.grid_rowconfigure(9, weight=1)
        metadata_window.grid_rowconfigure(10, weight=1)

        #Méta-données de la musique
        musique = music_tag.load_file(file_path)
        song_name = musique.raw["tracktitle"]
        artist_name = musique.raw["artist"]
        album_name = musique.raw["album"]
        album_artiste_name = musique.raw["albumartist"]
        compositor = musique.raw["composer"]
        genre = musique.raw["genre"]
        year = musique.raw["year"]
        track_number = musique.raw["tracknumber"]
        track_number_total = musique.raw["totaltracks"]
        disc_number = musique.raw["discnumber"]
        disc_number_total = musique.raw["totaldiscs"]
        comment = musique.raw["comment"]

        #Zone Cover + bouton Ecoute
        frame_cover_play = tk.Frame(metadata_window, bg="white")
        frame_cover_play.grid(row = 0, column = 0, pady=20, rowspan=11)

        #Label Cover de la musique
        #S'il y a une cover on l'affiche, sinon on affiche un placeholder
        if hasattr(musique["artwork"].first, "data"):
            image_donnee = musique["artwork"].first.data
            with open("images/cover.jpeg", "wb") as f:
                f.write(image_donnee)
            image = Image.open("images/cover.jpeg")
        else:
            image = Image.open("images/sans_cover.jpeg")
        #Pour conserver le ratio dans le cas où les covers ne sont pas carrés
        image.thumbnail((300, 300))
        cover_image = ImageTk.PhotoImage(image)
        cover_label = tk.Label(frame_cover_play, image=cover_image)
        cover_label.image = cover_image
        cover_label.grid(row = 0, column = 0, pady=(0,20))

        #Bouton Ecoute de la musique
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        image = Image.open("images/play.jpeg")
        image.thumbnail((50, 50))
        play_image = ImageTk.PhotoImage(image)
        image = Image.open("images/stop.jpeg")
        image.thumbnail((50, 50))
        stop_image = ImageTk.PhotoImage(image)
        def play():
            """!
            @brief Lancer l'écoute de la musique, en lien ave le bouton Ecoute
            """
            pygame.mixer.music.play()
            file_player_button.configure(image=stop_image, command=pause)
        def pause():
            """!
            @brief Mettre en pause l'écoute la musique
            """
            pygame.mixer.music.pause()
            file_player_button.configure(image=play_image, command=continu)
        def continu():
            """!
            @brief Reprendre l'écoute de la musique
            """
            pygame.mixer.music.unpause()
            file_player_button.configure(image=stop_image, command=pause)
        file_player_button = tk.Button(frame_cover_play, bg="white", highlightbackground="white", image=play_image, command=play)
        file_player_button.grid(row=1, column=0, pady=(20,0))
        #Pour que la musique s'arrête quand on quitte la fenêtre, sinon elle continue en arrière-plan...
        def on_closing():
            """!
            @brief Arrêter la musique quand la fenêtre se ferme
            """
            pygame.mixer.music.stop()
            metadata_window.destroy()
        metadata_window.protocol("WM_DELETE_WINDOW", on_closing)

        #Affichage des méta-données dans la fenêtre
        #Titre
        label_titre = tk.Label(metadata_window, text=f"Titre : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
        label_titre.grid(row=0, column=1, pady= 5, sticky = 'E')
        text_titre = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
        text_titre.grid(row=0, column=2, pady= 5, sticky = 'W')
        if song_name:
            text_titre.insert("1.0", song_name)

        #Artiste
        label_artiste = tk.Label(metadata_window, text=f"Artiste : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
        label_artiste.grid(row=1, column=1, pady= 5, sticky = 'E')
        text_artiste = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
        text_artiste.grid(row=1, column=2, pady= 5, sticky = 'W')
        if artist_name:
            text_artiste.insert("1.0", artist_name)

        #Album
        label_album = tk.Label(metadata_window, text=f"Album : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
        label_album.grid(row=2, column=1, pady= 5, sticky = 'E')
        text_album = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
        text_album.grid(row=2, column=2, pady= 5, sticky = 'W')
        if album_name:
            text_album.insert("1.0", album_name)

        #Artiste de l'album
        label_artiste_album = tk.Label(metadata_window, text=f"Artiste de l'album : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
        label_artiste_album.grid(row=3, column=1, pady= 5, sticky = 'E')
        text_artiste_album = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
        text_artiste_album.grid(row=3, column=2, pady= 5, sticky = 'W')
        if album_artiste_name:
            text_artiste_album.insert("1.0", album_artiste_name)

        #Compositeur
        label_compositeur = tk.Label(metadata_window, text=f"Compositeur : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
        label_compositeur.grid(row=4, column=1, pady= 5, sticky = 'E')
        text_compositeur = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
        text_compositeur.grid(row=4, column=2, pady= 5, sticky = 'W')
        if compositor:
            text_compositeur.insert("1.0", compositor)

        #Genre
        label_genre = tk.Label(metadata_window, text=f"Genre : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
        label_genre.grid(row=5, column=1, pady= 5, sticky = 'E')
        text_genre = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
        text_genre.grid(row=5, column=2, pady= 5, sticky = 'W')
        if genre:
            text_genre.insert("1.0", genre)

        #Année
        label_annee = tk.Label(metadata_window, text=f"Année :", bg= "white", fg="black", font=("Poppins", 14, "bold"))
        label_annee.grid(row=6, column=1, pady= 4, sticky = 'E')
        text_annee = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
        text_annee.grid(row=6, column=2, pady= 5, sticky = 'W')
        if year:
            text_annee.insert("1.0", year)

        #Piste
        label_piste = tk.Label(metadata_window, text=f"Piste : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
        label_piste.grid(row=7, column=1, pady= 5, sticky = 'E')
        frame_piste = tk.Frame(metadata_window, bg="white")
        frame_piste.grid(row=7, column=2, pady= 5, sticky = 'W')
        text_piste = tk.Text(frame_piste, width= 2, height=1, bg="white", fg="black", font=("Poppins", 14))
        text_piste.grid(row=0, column=0, pady= 5, sticky = 'W')
        label_sur_piste = tk.Label(frame_piste, text=" sur ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
        label_sur_piste.grid(row=0, column=1, pady= 5, sticky = 'W')
        text_piste_total = tk.Text(frame_piste, width= 2, height=1, bg="white", fg="black", font=("Poppins", 14))
        text_piste_total.grid(row=0, column=2, pady= 5, sticky = 'W')
        if track_number:
            text_piste.insert("1.0", track_number)
        if track_number_total:
            text_piste_total.insert("1.0", track_number_total)  

        #Numéro de disque
        label_numero_disque = tk.Label(metadata_window, text=f"Numéro de disque : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
        label_numero_disque.grid(row=8, column=1, pady= 5, sticky = 'E')
        frame_numero_disque = tk.Frame(metadata_window, bg="white")
        frame_numero_disque.grid(row=8, column=2, pady= 5, sticky = 'W')
        text_numero_disque = tk.Text(frame_numero_disque, width= 2, height=1, bg="white", fg="black", font=("Poppins", 14))
        text_numero_disque.grid(row=0, column=0, pady= 5, sticky = 'W')
        label_sur_numero_disque = tk.Label(frame_numero_disque, text=" sur ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
        label_sur_numero_disque.grid(row=0, column=1, pady= 5, sticky = 'W')
        text_numero_disque_total = tk.Text(frame_numero_disque, width= 2, height=1, bg="white", fg="black", font=("Poppins", 14))
        text_numero_disque_total.grid(row=0, column=2, pady= 5, sticky = 'W')
        if disc_number:
            text_numero_disque.insert("1.0", disc_number)
        if disc_number_total:
            text_numero_disque_total.insert("1.0", disc_number_total)
                
        #Commentaire
        label_comment = tk.Label(metadata_window, text=f"Commentaire : ", bg= "white", fg="black", font=("Poppins", 14, "bold"))
        label_comment.grid(row=9, column=1, pady= 5, sticky = 'E')
        text_comment = tk.Text(metadata_window, width= 30, height=1, bg="white", fg="black", font=("Poppins", 14))
        text_comment.grid(row=9, column=2, pady= 5, sticky = 'W')
        if comment:
            text_comment.insert("1.0", comment)

        #Enregistrer les méta-données
        def enregistrer_meta_donnees():
            """!
            @brief Commande du bouton Enregistrer : 
            Enregistrer les méta-données du fichier 
            en récupérant le contenu des champs de textes des méta-données
            """
            musique.raw["tracktitle"] = text_titre.get("1.0", "end")
            musique.raw["artist"] = text_artiste.get("1.0", "end")
            musique.raw["album"] = text_album.get("1.0", "end")
            musique.raw["albumartist"] = text_artiste_album.get("1.0", "end")
            musique.raw["composer"] = text_compositeur.get("1.0", "end")
            musique.raw["genre"] = text_genre.get("1.0", "end")
            musique.raw["year"] = text_annee.get("1.0", "end")
            musique.raw["discnumber"] = text_numero_disque.get("1.0", "end")
            musique.raw["comment"] = text_comment.get("1.0", "end")
            musique.save()
            messagebox.showinfo("Succès", "Opération d'enregistrement faite avec succès")

        #Bouton Enregistrer les méta-données
        button_enregistrer = tk.Button(metadata_window, fg="black", highlightbackground="white", compound="right", padx=10, pady=5,text="Enregistrer", command=enregistrer_meta_donnees)
        button_enregistrer.grid(row=10, column=2, padx=5, pady=5, sticky="W")

#Fenêtre Afficher les mp3/FLAC d'une arborescence d'un dossier à choisir
def select_folder():
    """!
    @brief Sélectionner un dossier et en extraire les mp3/FLAC pour les afficher
    """
    #Sélection du dossier
    folder_path = filedialog.askdirectory(title="Sélectionner un dossier")
    if not folder_path:
        messagebox.showwarning("Avertissement", "Aucun dossier sélectionné")
    else:
        #Fenêtre pour afficher les mp3/FLAC
        files_window = tk.Toplevel(root,  bg = "white")
        files_window.title("Liste des MP3/FLAC")
        files_window.geometry("500x500")
        #Le dictionnaire de sauvegarde des chemins absolus des mp3/FLAC
        audio_files_absolutes = {"chemin" : "chemin_absolu"}
        #Le dictionnaire d'exportation des mp3/FLAC en enlevant ou en rajoutant des chemins absolus à l'aide du dictionnaire de sauvegarde
        #Par défaut, il est identique au dictionnaire de sauvegarde, donc tous les mp3/FLAC sont à exporter
        switch_audio_files_absolutes = {}
        #Le tableau des chemins relatifs des mp3/FLAC
        audio_files = []
        #Remplissage des dictionnaires et du tableau
        for donnees in os.walk(folder_path):
            chemin, _, fichiers = donnees
            for f in fichiers:
                #Vérification de l'extension
                if f.lower().endswith(('.mp3', '.flac')):
                    le_chemin = os.path.join(chemin, f)
                    #Vérification du type MIME
                    type = mime.from_file(le_chemin)
                    if(type == "audio/mpeg" or type == "audio/flac" or type == "audio/x-flac"):
                        audio_files_absolutes[f]= le_chemin
                        switch_audio_files_absolutes[f] = le_chemin
                        audio_files.append(f)

        #Fonctions pour switch la commande du choix des mp3/FLAC à exporter
        def switchON(audio_file:str, switch_audio_file, index:int):
            """!
            @brief Rajoute le chemin absolu du mp3/FLAC dans le dictionnaire des mp3/FLAC à exporter
            @param audio_file le chemin relatif qui sert de clé au dictionnaire des mp3/FLAC (différent du dictionnaire à exporter) pour obtenir le chemin absolue
            @param switch_audio_file le bouton de sélection
            @param index l'indice pour manipuler le bon bouton
            """
            switch_audio_files_absolutes[audio_file] = audio_files_absolutes[audio_file]
            switch_audio_file.configure(text="O", command=lambda audio_file=audio_file, index=index: switchOFF(audio_file, liste_switch[index], index))
        def switchOFF(audio_file:str, switch_audio_file, index:int):
            """!
            @brief Enlève le chemin absolu du mp3/FLAC du dictionnaire des mp3/FLAC à exporter
            @param audio_file le chemin relatif qui sert de clé au dictionnaire des mp3/FLAC (différent du dictionnaire à exporter) pour obtenir le chemin absolue
            @param switch_audio_file le bouton de sélection
            @param index l'indice pour manipuler le bon bouton
            """
            switch_audio_files_absolutes.pop(audio_file, None)  # Utilisez .pop() avec un default pour éviter les KeyError
            switch_audio_file.configure(text="X", command=lambda audio_file=audio_file, index=index: switchON(audio_file, liste_switch[index], index))
        #Affichage des mp3/FLAC dans la fenêtre
        liste_switch = []
        i = 0
        #Zone de défilement pour les pistes
        tracks_frame = tk.Frame(files_window)
        tracks_frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(tracks_frame)
        scrollbar = tk.Scrollbar(tracks_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        for audio_file in audio_files:
            #Zone boutons mp3/FLAC + switch
            frame_buttons = tk.Frame(scrollable_frame, bg="white")
            frame_buttons.pack(padx=10, pady=10, anchor="w")
            #Bouton mp3/FLAC
            audio_button = tk.Button(frame_buttons,text=audio_file, bg='white', activebackground='white', highlightthickness=0, bd=0, border=0, font=("Poppins", 14), command=lambda t=audio_files_absolutes[audio_file]: select_file2(t))
            audio_button.grid(row=0, column=0, sticky="E")
            #Bouton Switch choix exportation du mp3/FLAC
            liste_switch.append(tk.Button(frame_buttons, text="O", bg='white', activebackground='white', highlightthickness=0, bd=0, border=0, font=("Poppins", 14), command=lambda audio_file=audio_file, i=i: switchOFF(audio_file, liste_switch[i], i)))
            liste_switch[i].grid(row=0, column=1, sticky="W")
            i += 1 

        #Exportation des mp3/FLAC sélectionnés dans un XSPF
        def export_audio_list():
            """!
            @brief Exporter les mp3/FLAC sélectionnés dans un XSPF
            """
            chemin = filedialog.asksaveasfilename(title="Enregistrer la liste des fichiers audio", filetypes=[("XSPF Files", "*.xspf")])
            if chemin:
                with open(chemin, "w", encoding="UTF-8") as file:
                    file.write('<?xml version="1.1" encoding="UTF-8"?>\n')
                    file.write('<playlist version="1" xmlns="http://xspf.org/ns/0/">\n')
                    file.write('  <trackList>\n')
                    for audio_chemin in switch_audio_files_absolutes.values():
                        file.write('    <track>\n')
                        file.write(f'      <location>{audio_chemin}</location>\n') # mettre file://
                        file.write(f'      <title>{os.path.basename(audio_chemin)}</title>\n')
                        file.write('    </track>\n')
                    file.write('  </trackList>\n')
                    file.write('</playlist>\n')
                    messagebox.showinfo("Succès", "Fichier XSPF enregistré")
            else:
                messagebox.showwarning("Avertissement", "Aucun fichier sélectionné")

        #Bouton Exporter les mp3/FLAC dans un XSPF
        export_button = tk.Button(files_window, fg="black", activebackground="firebrick1", activeforeground="white", highlightbackground="white", text="Exporter", command=export_audio_list, font=("Poppins", 14), border=0, image=iconExport, compound="right", padx=10, pady=5)
        export_button.pack(padx=10, pady=10, anchor="e")

#Fenêtre Afficher les mp3/FLAC d'un XSPF
def import_playlist():
    """!
    @brief Fonction pour importer une playlist XSPF
    """
    #On séléctionne le fichier XSPF à importer
    playlist = filedialog.askopenfilename(filetypes=[("Fichier XSPF", ".xspf")])
    if not playlist:
        messagebox.showwarning("Avertissement", "Aucun fichier XSPF sélectionné")
    else:
        #Lecture du fichier
        with open(playlist, "r") as fichier:
            #Le dictionnaire de sauvegarde des chemins absolus des mp3/FLAC
            audio_files_absolute = {"chemin" : "chemin_absolu"}
            #Le dictionnaire d'exportation des mp3/FLAC en enlevant ou en rajoutant des chemins absolus à l'aide du dictionnaire de sauvegarde
            #Par défaut, il est identique au dictionnaire de sauvegarde, donc tous les mp3/FLAC sont à exporter
            switch_audio_files_absolutes = {}
            #Le tableau des chemins relatifs des mp3/FLAC
            audio_files = []
            balise1 = "<location>"
            balise2 = "</location>"
            #On cherche les lignes avec les balises <location> qui ont le chemin absolu du mp3/FLAC
            for ligne in fichier:
                if balise1 in ligne:
                    index1 = ligne.index(balise1)
                    index2 = ligne.index(balise2)
                    chemin = ""
                    for index in range(index1 + len(balise1), index2):
                        chemin = chemin + ligne[index]
                    #Si le mp3/FLAC a été déplacé ou supprimé, on ne le compte pas
                    if(os.path.lexists(chemin.strip())):
                        #Vérification du type MIME au cas où le fichier aurait été remplacé par un faux qui a le même nom
                        type = mime.from_file(chemin)
                        if(type == "audio/mpeg" or type == "audio/flac" or type == "audio/x-flac"):
                            audio = os.path.basename(chemin)
                            audio_files_absolute[audio] = chemin
                            switch_audio_files_absolutes[audio] = chemin
                            audio_files.append(audio)

        #Fenêtre pour afficher les mp3/FLAC
        files_window = tk.Toplevel(root,  bg = "white")
        files_window.title("Liste des MP3/FLAC")
        files_window.geometry("500x500")

        #Fonctions pour switch la commande du choix des mp3/FLAC à exporter
        def switchON(audio_file, switch_audio_file, index):
            """!
            @brief Rajoute le chemin absolu du mp3/FLAC dans le dictionnaire des mp3/FLAC à exporter
            @param audio_file le chemin relatif qui sert de clé au dictionnaire des mp3/FLAC (différent du dictionnaire à exporter) pour obtenir le chemin absolue
            @param switch_audio_file le bouton de sélection
            @param index l'indice pour manipuler le bon bouton
            """
            switch_audio_files_absolutes[audio_file] = audio_files_absolute[audio_file]
            switch_audio_file.configure(text="O", command=lambda audio_file=audio_file, index=index: switchOFF(audio_file, liste_switch[index], index))
        def switchOFF(audio_file, switch_audio_file, index):
            """!
            @brief Enlève le chemin absolu du mp3/FLAC du dictionnaire des mp3/FLAC à exporter
            @param audio_file le chemin relatif qui sert de clé au dictionnaire des mp3/FLAC (différent du dictionnaire à exporter) pour obtenir le chemin absolue
            @param switch_audio_file le bouton de sélection
            @param index l'indice pour manipuler le bon bouton
            """
            switch_audio_files_absolutes.pop(audio_file, None)  #Avec un default pour éviter les KeyError
            switch_audio_file.configure(text="X", command=lambda audio_file=audio_file, index=index: switchON(audio_file, liste_switch[index], index))

        #Affichage des mp3/FLAC dans la fenêtre
        liste_switch = []
        i = 0
        #Zone de défilement pour les pistes
        tracks_frame = tk.Frame(files_window)
        tracks_frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(tracks_frame)
        scrollbar = tk.Scrollbar(tracks_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        for audio_file in audio_files:
            #Zone boutons mp3/FLAC + switch
            frame_buttons = tk.Frame(scrollable_frame, bg="white")
            frame_buttons.pack(padx=10, pady=10, anchor="w")
            #Bouton mp3/FLAC
            audio_button = tk.Button(frame_buttons,text=audio_file, bg='white', activebackground='white', highlightthickness=0, bd=0, border=0, font=("Poppins", 14), command=lambda t=audio_files_absolute[audio_file]: select_file2(t))
            audio_button.grid(row=0, column=0, sticky="E")
            #Bouton Switch choix exportation du mp3/FLAC
            liste_switch.append(tk.Button(frame_buttons, text="O", bg='white', activebackground='white', highlightthickness=0, bd=0, border=0, font=("Poppins", 14), command=lambda audio_file=audio_file, i=i: switchOFF(audio_file, liste_switch[i], i)))
            liste_switch[i].grid(row=0, column=1, sticky="W")
            i += 1 

        #Exportation des mp3/FLAC sélectionnés dans un XSPF
        def export_audio_list():
            """!
            @brief Exporter les mp3/FLAC sélectionnés dans un XSPF
            """
            chemin = filedialog.asksaveasfilename(title="Enregistrer la liste des fichiers audio", filetypes=[("XSPF Files", "*.xspf")])
            if chemin:
                with open(chemin, "w", encoding="UTF-8") as file:
                    file.write('<?xml version="1.1" encoding="UTF-8"?>\n')
                    file.write('<playlist version="1" xmlns="http://xspf.org/ns/0/">\n')
                    file.write('  <trackList>\n')
                    for audio_chemin in switch_audio_files_absolutes.values():
                        file.write('    <track>\n')
                        file.write(f'      <location>{audio_chemin}</location>\n') # mettre file://
                        file.write(f'      <title>{os.path.basename(audio_chemin)}</title>\n')
                        file.write('    </track>\n')
                    file.write('  </trackList>\n')
                    file.write('</playlist>\n')
                    messagebox.showinfo("Succès", "Fichier XSPF enregistré")
            else:
                messagebox.showwarning("Avertissement", "Aucun fichier sélectionné")

        #Bouton Exporter les mp3/FLAC dans un XSPF
        export_button = tk.Button(files_window, fg="black", activebackground="firebrick1", activeforeground="white", highlightbackground="white", text="Exporter", command=export_audio_list, font=("Poppins", 14), border=0, image=iconExport, compound="right", padx=10, pady=5)
        export_button.pack(padx=10, pady=10, anchor="e")

#Afficher des labels de méta-données d'un album lié à la recherche
def display_metadata(window, label_text:str, metadata:str):
    """!
    @brief Afficher une méta-donnée dans la fenêtre 
    @param window Fenêtre où afficher la méta-donnée
    @param label_text Texte du label à afficher
    @param metadata Méta-donnée à afficher
    """
    label = tk.Label(window, text=f"{metadata}", font=("Poppins", 14), fg="black")
    label_text_widget = tk.Label(window, text=label_text, font=("Poppins", 14, "bold"), fg="black")
    label_text_widget.pack(padx=20, pady=2, anchor='w')
    label.pack(padx=20, pady=2, anchor='w')

#Fenêtre Afficher les albums correspondant à une recherche
def search_album():
    """!
    @brief Rechercher les métadonnées d'un album
    """
    #Fenêtre Recherche
    search_window = tk.Toplevel(root)
    search_window.title("Rechercher un album")
    search_window.geometry("800x800")
    search_window.resizable(False, False) #bloquer le redimensionnement de la fenêtre
    
    #Label de la fenêtre Recherche
    search_label = tk.Label(search_window, text="Rechercher un album", font=("Poppins", 16, "bold"), fg="black", image=iconButton4, compound="right")
    search_label.pack(padx=20, pady=20, anchor='w')
    
    #Barre de recherche de la fenêtre Recherche
    search_entry = tk.Entry(search_window, font=("Poppins", 14), width=50)
    search_entry.pack(padx=20,pady=10, anchor='w')
    
    #Bouton Rechercher
    search_button = tk.Button(search_window, text="Rechercher", command=lambda: api_search_album(search_entry.get()), font=("Poppins", 14), fg="black")
    search_button.pack(padx=20,pady=10, anchor='w')
    
    results_label = tk.Label(search_window, text="", font=("Poppins", 14), fg="black")
    results_label.pack(padx=20,pady=10, anchor='w')

    def show_album(album):
        """!
        @brief Afficher les données d'un album
        @param album l'album à afficher
        """
        #Fenêtre Données de l'album
        metadata_window = tk.Toplevel(search_window)
        metadata_window.title("Détails de l'album")
        metadata_window.geometry("500x750")

        #Récupération des méta-données de l'album
        data = requests.get(album['tracklist'])
        if data.status_code == 200:
            tracks = data.json()['data']
            response = requests.get(album['cover_medium'])
            if response.status_code == 200:
                with open("images/cover.jpg", "wb") as file:
                    file.write(response.content)
                image = Image.open("images/cover.jpg")
                cover_image = ImageTk.PhotoImage(image)
                cover_label = tk.Label(metadata_window, image=cover_image)
                cover_label.image = cover_image
                cover_label.pack(pady=20, anchor='w', padx=20)
            genre = requests.get(f"https://api.deezer.com/genre/0{album['genre_id']}")
            genre = genre.json()['name']

            #Afficher les méta-données de l'album
            display_metadata(metadata_window, "Titre de l'album", album['title'])
            display_metadata(metadata_window, "Artiste", album['artist'])
            display_metadata(metadata_window, "Nombre de pistes", f"{album['nb_tracks']} pistes") 
            display_metadata(metadata_window, "Genre", genre)
            
            #Label de la fenêtre Données de l'album
            text = tk.Label(metadata_window, text="Pistes", font=("Poppins", 14, "bold"), fg="black", anchor='w')
            text.pack(pady=10, anchor='w', padx=20)
            
            #Zone de défilement pour les pistes
            tracks_frame = tk.Frame(metadata_window)
            tracks_frame.pack(pady=10, fill=tk.BOTH, expand=True)
            canvas = tk.Canvas(tracks_frame)
            scrollbar = tk.Scrollbar(tracks_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
            #Afficher les pistes
            for track in tracks:
                result_text = f"{track['title']} - {track['duration'] // 60}:{track['duration'] % 60:02d}"
                result_label = tk.Label(scrollable_frame, text=result_text, font=("Poppins", 14), fg="black")
                result_label.pack(pady=5, padx=20, anchor='w')

    def api_search_album(query:str):
        """!
        @brief Rechercher un album sur Deezer par son nom en entrée et afficher les albums qui pourraient correspondre à la recherche
        @param query le nom de l'album à rechercher
        """
        #Récupération des albums qui pourraient correspondre à la recherche
        albums = []
        url = f"https://api.deezer.com/search/album?q={query}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for album in data['data']:
                albums.append({
                    'id': album['id'],
                    'title': album['title'],
                    'artist': album['artist']['name'],
                    'tracklist': album['tracklist'],
                    'nb_tracks': album['nb_tracks'],
                    'cover_medium': album['cover_medium'],
                    'genre_id': album['genre_id']
                })
            results_label.config(text="")
            #Supprime les widgets de la fenêtre pour laisser place aux résultats de recherche
            for widget in search_window.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.destroy()
            
            #Zone de défilement pour les résultats de recherche
            results_frame = tk.Frame(search_window)
            results_frame.pack(pady=10, fill=tk.BOTH, expand=True)
            canvas = tk.Canvas(results_frame)
            scrollbar = tk.Scrollbar(results_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            #Afficher les albums qui pourraient correspondre à la recherche
            for album in albums:
                result_text = f"{album['title']} - {album['artist']} ({album['nb_tracks']} pistes)"
                result_button = tk.Button(scrollable_frame, text=result_text, font=("Poppins", 14), fg="black", command=lambda t=album: show_album(t))
                result_button.pack(pady=5, padx=20, anchor='w')

#La suite du menu principal
#Bouton Afficher les méta-données d'un mp3/FLAC
file_button = tk.Button(root, text="Afficher les méta-données d'un MP3/FLAC", command=select_file, font=("Poppins", 14), bg="white", fg="black", highlightbackground="white", image=iconButton1, compound="right", padx=10, pady=5)
file_button.pack(pady=10)

#Bouton Extraire les mp3/FLAC d'un dossier et les afficher
folder_button = tk.Button(root, text="Lister les MP3/FLAC d'un dossier", command=select_folder, font=("Poppins", 14), bg="white", fg="black", highlightbackground="white", image=iconButton2, compound="right", padx=10, pady=5)
folder_button.pack(pady=10)

#Bouton Importer une playlist XSPF et en afficher les mp3/FLAC
folder_button = tk.Button(root, text="Importer une playlist", command=import_playlist, font=("Poppins", 14), bg="white", fg="black", highlightbackground="white", image=iconButton3, compound="right", padx=10, pady=5)
folder_button.pack(pady=10)

#Bouton Recherche des informations d'un album via API et les afficher
folder_button = tk.Button(root, text="Rechercher les informations d'un album", command=search_album, font=("Poppins", 14), bg="white", fg="black", highlightbackground="white", image=iconButton4, compound="right", padx=10, pady=5)
folder_button.pack(pady=10)

#Lancer l'interface graphique
root.mainloop()
