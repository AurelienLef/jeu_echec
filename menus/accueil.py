import tkinter as tk


class accueil:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("750x750")
        self.click = 0

        button = tk.Button(self.root, text="BIENVENUE SUR CHESS\nCliquez pour continuer", font=("Nunito", 40),
                           fg="white", activeforeground="white", bg="#67A032", activebackground="#67A032",
                           command=self.est_click)

        button.pack(expand=True, fill="both")

        self.root.mainloop()

    def est_click(self):
        self.click = 1
        self.root.destroy()

    def result_click(self):
        return self.click
