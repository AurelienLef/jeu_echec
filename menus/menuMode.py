import tkinter as tk

class menuMode:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("750x750")
        self.root.config(bg="#67A032")
        self.choix = "facile"
        self.couleur = "Blanc"
        self.ferme = 1

        text = tk.Label(self.root, text="Choisir le mode", font=("Nunito", 45), fg="white", bg="#67A032")
        text.place(x=140, y=50)

        retour_btn = tk.Button(self.root, text="Retour", font=("Nunito", 15), bg="#E7E4E2", bd=0, width=10, height=1, command=self.choose6)
        retour_btn.place(x=290, y=575)

        self.canvas1 = tk.Canvas(self.root, width=60, height=60)
        self.canvas1.place(x=142, y=160)
        self.case_facile = self.canvas1.create_rectangle(60, 60, 60, 60, width=120, outline="black")
        facile_btn = tk.Button(self.root, text="Aléatoire", font=("Nunito", 15), bg="#E7E4E2", bd=0, width=20, height=2, command=self.choose1)
        facile_btn.place(x=232, y=160)

        self.canvas2 = tk.Canvas(self.root, width=60, height=60)
        self.canvas2.place(x=142, y=235)
        self.case_difficile = self.canvas2.create_rectangle(60, 60, 60, 60, width=120, outline="white")
        difficile_btn = tk.Button(self.root, text="MinMax", font=("Nunito", 15), bg="#E7E4E2", bd=0, width=20, height=2, command=self.choose2)
        difficile_btn.place(x=232, y=235)

        self.canvas3 = tk.Canvas(self.root, width=60, height=60)
        self.canvas3.place(x=142, y=310)
        self.case_ia = self.canvas3.create_rectangle(60, 60, 60, 60, width=120, outline="white")
        ia_btn = tk.Button(self.root, text="Contre un Joueur", font=("Nunito", 15), bg="#E7E4E2", bd=0, width=20, height=2, command=self.choose3)
        ia_btn.place(x=232, y=310)

        self.couleur_btn = tk.Button(self.root, text="Pions Blanc", font=("Nunito", 15), bg="#E7E4E2", bd=0, width=20, height=2, command=self.choose4)
        self.couleur_btn.place(x=232, y=385)

        jouer_btn = tk.Button(self.root, text="Jouer", font=("Nunito", 15), bg="#E7E4E2", bd=0, width=20, height=2, command=self.choose5)
        jouer_btn.place(x=232, y=460)

        self.root.mainloop()

    def result_choix(self):
        return self.choix, self.couleur, self.ferme

    def choose1(self):
        self.choix = "facile"
        self.canvas1.itemconfig(self.case_facile, outline="black")
        self.canvas2.itemconfig(self.case_facile, outline="white")
        self.canvas3.itemconfig(self.case_facile, outline="white")

    def choose2(self):
        self.choix = "difficile"
        self.canvas1.itemconfig(self.case_facile, outline="white")
        self.canvas2.itemconfig(self.case_facile, outline="black")
        self.canvas3.itemconfig(self.case_facile, outline="white")

    def choose3(self):
        self.choix = "joueur"
        self.canvas1.itemconfig(self.case_facile, outline="white")
        self.canvas2.itemconfig(self.case_facile, outline="white")
        self.canvas3.itemconfig(self.case_facile, outline="black")

    def choose4(self):
        if self.couleur == "Blanc":
            self.couleur = "Noir"
            self.couleur_btn.config(text="Pions Noir")
        else:
            self.couleur = "Blanc"
            self.couleur_btn.config(text="Pions Blanc")

    def choose5(self):
        self.ferme = 0
        self.root.destroy()

    def choose6(self):
        self.choix = "retour"
        self.root.destroy()
