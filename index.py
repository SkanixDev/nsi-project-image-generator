# Importation des modules nécessaires
import tkinter
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageDraw
import os

# Création d'une fenêtre
win = tkinter.Tk()
# Titre de la fenêtre
win.title("Projet de NSI - Modification d'image")
# Format de la fenêtre
win.geometry('400x200')
# Couleur de fond de la fenêtre
win.configure(bg='grey')
# Empêcher le redimensionnement de la fenêtre
win.resizable(False, False)
# Ajout d'un logo
win.iconbitmap('logo.ico')

# Création de la fonction pour récupérer le chemin d'accès du fichier


def get_file_path(reopen=0):
    for widget in win.winfo_children():
        widget.destroy()
    # Passage à la fenêtre pour choisir les lignes et inverser ou pas

    def valider():
        # -------------------------------------------- #
        # Lancement de l'algorithme
        # -------------------------------------------- #

        def show_values():
            # Ouverture de la Progression
            popup = Toplevel()
            popup.title("Progression")
            popup.geometry("300x100")
            popup.configure(bg='grey')
            popup.resizable(False, False)
            texte = Label(popup, text="Chargement de l'image...",
                          font=("Calibri", 10), bg="grey", fg="white")
            texte.pack(pady=10)

            progress = ttk.Progressbar(popup, orient=HORIZONTAL,
                                       length=300, mode='determinate')
            progress.pack(pady=20)
            progress['value'] = 0
            progress['maximum'] = 100

            # Chargement image, récupération des pixels
            im = Image.open(file_path)
            pix = im.load()

            width, height = im.size

            # Récupération de 10 lignes de pixels
            def linesOfPixels(y, num_lines=10):
                lines = []
                for i in range(y, min(y+num_lines, height)):
                    line = []
                    for pixel in range(width):
                        line.append(pix[pixel, i])
                    lines.append(line)
                return lines

            # Moyenne des couleurs d'une partie de l'image
            def moyenne_pixel(list_pixels):
                r = 0
                g = 0
                b = 0
                for pixel in list_pixels:
                    r += pixel[0]
                    g += pixel[1]
                    b += pixel[2]
                return (round(r/len(list_pixels)), round(g/len(list_pixels)), round(b/len(list_pixels)))

            images = []
            num_of_row = curseur.get()

            # Remplacement de l'image par rectangle de couleur
            for y in range(0, height, num_of_row):
                newImg = Image.new('RGB', (width, height), (0, 0, 0))
                imgDraw = ImageDraw.Draw(newImg)
                newImg.paste(im)
                for i in range(0, y+1, num_of_row):
                    lines = linesOfPixels(i, num_lines=num_of_row)
                    moyenne = moyenne_pixel(
                        [pixel for line in lines for pixel in line])
                    imgDraw.rectangle(
                        (0, i, width, min(i+num_of_row, height)), fill=moyenne)
                    print("y:", y, "i:", i)
                images.append(newImg)
                # Avancement de la progressBar
                progress['value'] = progress['value'] + 100/height*num_of_row
                popup.update()

            if inverserValue.get() == 1:
                # Ajouter à la liste les même image à l'envers
                reverse_img = images

                print("Reverse Img", images)
                print("Reverse Img", list(reversed(reverse_img)))
                reverse_img = list(reversed(reverse_img))

                for x in reverse_img:
                    images.append(x)
                    print("Image add")

            # Enregistrement du GIF
            images[0].save('./newImage.gif',
                           save_all=True, append_images=images[1:], optimize=True, duration=40, loop=0, quality=50)

            # Changement du texte de la fenêtre
            popup.title("Traitement de l'image terminé !")
            texte.configure(text="Traitement de l'image terminé !")

            # -------------------------------------------- #
            # Lancement de l'algorithme
            # -------------------------------------------- #

            # Fermeture de la fenêtre de progression après 2 secondes
            win.after(2000, popup.destroy)

            def open_image():
                # Ouverture de l'image
                os.system("start ./newImage.gif")

            # Changement de la fenêtre de l'application
            win.geometry('600x100')
            win.resizable(False, False)
            curseur.destroy()
            inverser.destroy()
            valider2.destroy()
            texte2.destroy()

            texteTitle2.configure(
                text="Merci d'avoir utilisé notre application !")
            # bouton fermer et ouvrir l'image en bas de la page
            fermer = Button(win, text="Fermer", font=(
                'Calibri', 10), command=win.destroy)
            fermer.place(relx=0.6, rely=0.8, anchor="center")
            ouvrir = Button(win, text="Ouvrir l'image", font=(
                'Calibri', 10), command=open_image)
            ouvrir.place(relx=0.4, rely=0.8, anchor="center")
        e1.destroy()
        autrechoix.destroy()
        valider.destroy()
        win.geometry('600x300')
        texteTitle2 = Label(win, text="Choisissez le nombre de lignes de pixels floutées :", font=(
            'Calibri', 20, "bold"), bg="grey", fg="white")
        texteTitle2.place(relx=0.5, rely=0.3, anchor="center")
        curseur = Scale(win, from_=1, to=200, length=300, orient=HORIZONTAL)
        curseur.place(relx=0.5, rely=0.5, anchor="center")
        texte2 = Label(win, text="(une petite quantité de lignes entraîne un chargement court mais une image pixellisée, et inversement)", font=(
            'Calibri', 10), bg="grey", fg="white")
        texte2.place(relx=0.5, rely=0.6, anchor="center")
        inverserValue = tkinter.IntVar()
        inverser = Checkbutton(win, text='Inverser',
                               variable=inverserValue, onvalue=1, offvalue=0)
        inverser.place(relx=0.25, rely=0.8, anchor='center')
        valider2 = Button(win, text='Valider', command=show_values)
        valider2.place(relx=0.75, rely=0.8, anchor="center")

    global file_path
    # Variable dans laquelle va être stocké le chemin d'accès (ouvre l'explorateur de fichiers)
    file_path = filedialog.askopenfilename(
        title='Choisissez un fichier image', filetypes=[('Images', '*.png', 'JPEG')])
    # catch si l'utilisateur annule l'ouverture de l'image
    if file_path == "":
        return main()
    # Récupère l'image
    img = Image.open(file_path)
    # Récupère la taille de l'image
    width, height = img.size
    # Définit une nouvelle largeur
    width_new = int(390)
    # Définit une nouvelle hauteur (en gardant les proportions de l'image)
    height_new = int(height*390/width)
    # Modifie la taille de l'image avec les nouvelles largeur et hauteur
    img_resized = img.resize((width_new, height_new))
    # Transforme l'image en image exploitable par Tkinter
    img_resized = ImageTk.PhotoImage(img_resized)
    # Création d'un widget
    e1 = Label(win)
    # Placement du widget
    e1.grid(row=0, column=0, columnspan=2, padx=3, pady=3)
    # Attache l'image au widget
    e1.image = img_resized
    # Affiche l'image
    e1['image'] = img_resized
    # Définit une nouvelle taille de fenêtre (adaptée à l'image)
    d = "400x"+str(height_new+50)
    # Applique la nouvelle taille de fenêtre
    win.geometry(d)
    # Supprime le bouton qui ouvre l'explorateur de fichiers
    button.destroy()
    # Supprime le texte "Choisissez une image à modifier :"
    texte1.destroy()
    # Création du bouton valider
    valider = Button(win, text="Valider", font=(
        'Calibri', 10), command=valider)
    # Placement du bouton valider
    valider.grid(row=1, column=1, padx=3, pady=3)
    # Création du bouton "Choisir une autre image"
    autrechoix = Button(win, text="Choisir une autre image",
                        font=('Calibri', 10), command=get_file_path)
    # Placement du bouton "Choisir une autre image"
    autrechoix.grid(row=1, column=0, padx=3, pady=3)


def main():
    global button, texte1
    # Création du bouton qui ouvre l'explorateur de fichiers
    button = Button(win, text="Ouvrir l'explorateur de fichiers",
                    font=('Calibri', 10), command=get_file_path)
    # Placement du bouton qui ouvre l'explorateur de fichiers
    button.place(relx=0.5, rely=0.4, anchor="center")

    # Création du bouton pour fermer l'application
    button = Button(win, text="Quitter",
                    font=('Calibri', 10), command=win.destroy)
    # Placement du bouton qui quitte l'application
    button.place(relx=0.5, rely=0.8, anchor="center")

    # Création du texte "Choisissez une image à modifier :"
    texte1 = Label(win, text="Choisissez une image à modifier :",
                   font=('Calibri', 17, "bold"), bg="grey", fg="white")
    # Placement du texte "Choisissez une image à modifier :"
    texte1.place(relx=0.5, rely=0.2, anchor="center")


main()

win.mainloop()
