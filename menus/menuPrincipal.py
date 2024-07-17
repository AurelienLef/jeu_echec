import tkinter as tk
from tkinter import messagebox
import webbrowser


class menuPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("750x750")
        self.root.config(bg="#67A032")
        self.choix = 0

        text = tk.Label(self.root, text="Bienvenue sur ce jeu", font=("Nunito", 45), fg="white", bg="#67A032")
        joue_btn = tk.Button(self.root, text="Jouer une partie", font=("Nunito", 15), bg="#E7E4E2", bd=0, width=20, height=2, command=self.choose1)
        continue_btn = tk.Button(self.root, text="Continuer une partie", font=("Nunito", 15), bg="#E7E4E2", bd=0, width=20, height=2, command=self.choose2)
        regle_btn = tk.Button(self.root, text="Règles du jeu", font=("Nunito", 15), bg="#E7E4E2", bd=0, width=20, height=2, command=self.choose3)
        quitter_btn = tk.Button(self.root, text="Quitter le jeu", font=("Nunito", 15), bg="#E7E4E2", bd=0, width=20, height=2, command=self.choose4)

        text.place(x=55, y=50)
        joue_btn.place(x=232, y=160)
        continue_btn.place(x=232, y=235)
        regle_btn.place(x=232, y=310)
        quitter_btn.place(x=232, y=385)

        self.root.mainloop()

    def result_choix(self):
        print(self.choix)
        return self.choix

    def choose1(self):
        self.choix = "jouer"
        self.root.destroy()

    def choose2(self):
        self.choix = "continuer"
        self.root.destroy()

    def choose3(self):
        self.choix = "regle"
        root_qst = tk.Tk()
        root_qst.withdraw()
        fin = messagebox.showinfo("Annonce des règles", "Vous allez être redirigé vers un site web.")
        root_qst.destroy()
        url = "http://www.echecs.asso.fr/livrearbitre/110.pdf"
        webbrowser.open(url)

    def choose4(self):
        self.choix = "quitter"
        self.root.destroy()
