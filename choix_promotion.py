import tkinter as tk

class choix_promo:
    def __init__(self, joue):
        self.root = tk.Tk()

        self.choix = 0
        self.joue = joue

        if joue % 2 == 0:
            img1 = tk.PhotoImage(file="pieces_echec/dameB.png")
            img2 = tk.PhotoImage(file="pieces_echec/tourB.png")
            img3 = tk.PhotoImage(file="pieces_echec/fouB.png")
            img4 = tk.PhotoImage(file="pieces_echec/cavalierB.png")
        else:
            img1 = tk.PhotoImage(file="pieces_echec/dameN.png")
            img2 = tk.PhotoImage(file="pieces_echec/tourN.png")
            img3 = tk.PhotoImage(file="pieces_echec/fouN.png")
            img4 = tk.PhotoImage(file="pieces_echec/cavalierN.png")

        self.img_rz1 = img1.zoom(2, 2)
        self.img_rz2 = img2.zoom(2, 2)
        self.img_rz3 = img3.zoom(2, 2)
        self.img_rz4 = img4.zoom(2, 2)

        button1 = tk.Button(self.root, image=self.img_rz1, command=self.choose1)
        button2 = tk.Button(self.root, image=self.img_rz2, command=self.choose2)
        button3 = tk.Button(self.root, image=self.img_rz3, command=self.choose3)
        button4 = tk.Button(self.root, image=self.img_rz4, command=self.choose4)

        button1.grid(row=0, column=0)
        button2.grid(row=0, column=1)
        button3.grid(row=1, column=0)
        button4.grid(row=1, column=1)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def result_choix(self):
        return self.choix

    def choose1(self):
        self.choix = "dame"
        self.root.destroy()


    def choose2(self):
        self.choix = "tour"
        self.root.destroy()


    def choose3(self):
        self.choix = "fou"
        self.root.destroy()


    def choose4(self):
        self.choix = "cavalier"
        self.root.destroy()

    def on_closing(self):
        print("Promotion obligatoire")

