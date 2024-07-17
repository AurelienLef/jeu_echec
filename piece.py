import pygame
import os

class piece:
    def __init__(self, nom, couleur, posX=0, posY=0, decalX=0, decalY=0,etat=-1,taille=80):
        self.nom = nom
        self.couleur = couleur
        self.taille = taille
        path = os.path.join(os.getcwd(), "pieces_echec")
        self.img = pygame.image.load(f"{path}/{self.nom}{self.couleur[0]}.png")
        self.img = pygame.transform.scale(self.img, (taille, taille))
        self.decalX = decalX
        self.decalY = decalY
        self.posX = posX
        self.posY = posY
        self.estSelect = 0
        if(etat==-1):
            self.etat = 1 if self.nom == "tour" or self.nom == "pion" or self.nom == "roi" else 0
        else:
            self.etat = etat

    def ecrit(self):
        return self.nom+" "+self.couleur+" "+str(self.posY)+"-"+str(self.posX)+" "+str(self.etat)

    def getCol(self):
        return int((self.posX - self.decalX) // 8)

    def getRow(self):
        return int((self.posY - self.decalY) // 8)
