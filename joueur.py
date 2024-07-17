from piece import piece

class joueur:
    def __init__(self, nom, couleur="Blanc",difficulter="facile"):
        self.nom = nom
        self.couleur = couleur
        self.pieceAdverse = []
        self.difficulter=difficulter

