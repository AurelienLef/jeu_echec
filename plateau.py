
from curses import mouseinterval
from genericpath import exists
from json import dump
import json
import os
import pygame
import tkinter as tk
from tkinter import messagebox
import random
import time
from piece import piece
from plateauMinMax import plateauMinMax
from button import button
from choix_promotion import choix_promo
import copy

class plateau:
    def __init__(self, nom, tailleC, J, screen, dX, dY):
        self.nom = nom
        self.tailleCase = tailleC
        self.couleurJ = J.couleur
        self.J=J
        self.couleurHaut = "Blanc" if self.couleurJ == "Noir" else "Noir"
        self.joue = 0
        self.pieces_mangees = []
        self.screen = screen
        self.cases = []
        self.decalX = dX
        self.decalY = dY
        self.defini_cases()
        self.boutonQuit = button("Quitter la partie", 1165, 30, 200, 70, self.screen)

        self.P=100
        self.C=305
        self.F=333
        self.T=563
        self.D=950

    def defini_cases(self):
        listePiece = ["tour", "cavalier", "fou", "dame", "roi", "fou", "cavalier", "tour", "pion"]
        for row in range(8):
            listeTMP = []
            for column in range(8):
                if row == 0:
                    couleur = "Blanc" if self.couleurJ == "Noir" else "Noir"
                    listeTMP.append(piece(listePiece[column], couleur, column, row, self.decalX, self.decalY))
                elif row == 1:
                    couleur = "Blanc" if self.couleurJ == "Noir" else "Noir"
                    listeTMP.append(piece(listePiece[8], couleur, column, row, self.decalX, self.decalY))
                elif row == 6:
                    listeTMP.append(piece(listePiece[8], self.couleurJ, column, row, self.decalX, self.decalY))
                elif row == 7:
                    listeTMP.append(piece(listePiece[column], self.couleurJ, column, row, self.decalX, self.decalY))
                else:
                    listeTMP.append(False)
            self.cases.append(listeTMP)

    def recherche_piece(self, nom, couleur):
        for col in range(8):
            for row in range(8):
                if self.cases[row][col] and self.cases[row][col].nom == nom and self.cases[row][col].couleur == couleur:
                    return True
        return False

    def bon_joueur(self, p):
        if (self.joue % 2 == 0 and p.couleur == "Blanc") or (self.joue % 2 == 1 and p.couleur == "Noir"):
            return 1
        return 0

    def select(self, p):
        self.unselect(p)

        if self.bon_joueur(p):
            p.estSelect = 1 if p.estSelect == 0 else 0

    def unselect(self, p):
        for col in range(8):
            for row in range(8):
                if self.cases[row][col] and self.cases[row][col].estSelect == 1:
                    self.cases[row][col].estSelect = 0

    def isSelect(self):
        p = False
        for col in range(0, 8):
            for row in range(0, 8):
                if self.cases[col][row] and self.cases[col][row].estSelect == 1:
                    p = self.cases[col][row]

        return p if p else False

    def promotion(self, p):
        if p.couleur == self.couleurJ or self.J.difficulter=="joueur":
            choose = choix_promo(self.joue)
            promue = choose.result_choix()
        else:
            promo = ["dame", "tour", "fou", "cavalier"]
            promue = random.choice(promo)

        coul = "Blanc" if self.joue % 2 == 0 else "Noir"
        new_piece = piece(promue, coul, p.posX, p.posY, self.decalX, self.decalY)
        return new_piece

    def mouvementManuel(self, ligne, colonne, nouvelleLigne, nouvelleColonne):
        if (self.cases[ligne][colonne] == False):
            return False
        else:
            p = self.cases[ligne][colonne]
            self.cases[ligne][colonne] = False
            p.posY, p.posX = nouvelleLigne, nouvelleColonne
            self.cases[nouvelleLigne][nouvelleColonne] = p
            return True

    def visionDiagonale(self, l, c, p):
        resultList = []
        lTMP = l + 1
        cTMP = c + 1
        while (lTMP != 8 and cTMP != 8 and self.cases[lTMP][cTMP] == False):
            resultList.append((lTMP, cTMP))
            lTMP += 1
            cTMP += 1
        if (lTMP != 8 and cTMP != 8 and self.cases[lTMP][cTMP] != False and self.cases[lTMP][
            cTMP].couleur != p.couleur):
            resultList.append((lTMP, cTMP))

        lTMP = l - 1
        cTMP = c + 1
        while (lTMP != -1 and cTMP != 8 and self.cases[lTMP][cTMP] == False):
            resultList.append((lTMP, cTMP))
            lTMP -= 1
            cTMP += 1
        if (lTMP != -1 and cTMP != 8 and self.cases[lTMP][cTMP] != False and self.cases[lTMP][
            cTMP].couleur != p.couleur):
            resultList.append((lTMP, cTMP))

        lTMP = l - 1
        cTMP = c - 1
        while (lTMP != -1 and cTMP != -1 and self.cases[lTMP][cTMP] == False):
            resultList.append((lTMP, cTMP))
            lTMP -= 1
            cTMP -= 1
        if (lTMP != -1 and cTMP != -1 and self.cases[lTMP][cTMP] != False and self.cases[lTMP][
            cTMP].couleur != p.couleur):
            resultList.append((lTMP, cTMP))

        lTMP = l + 1
        cTMP = c - 1
        while (lTMP != 8 and cTMP != -1 and self.cases[lTMP][cTMP] == False):
            resultList.append((lTMP, cTMP))
            lTMP += 1
            cTMP -= 1
        if (lTMP != 8 and cTMP != -1 and self.cases[lTMP][cTMP] != False and self.cases[lTMP][
            cTMP].couleur != p.couleur):
            resultList.append((lTMP, cTMP))

        return resultList

    def visionLigne(self, l, c, p):
        resultList = []
        lTMP = l + 1
        while (lTMP != 8 and self.cases[lTMP][c] == False):
            resultList.append((lTMP, c))
            lTMP += 1
        if (lTMP != 8 and self.cases[lTMP][c].couleur != p.couleur):
            resultList.append((lTMP, c))

        lTMP = l - 1
        while (lTMP != -1 and self.cases[lTMP][c] == False):
            resultList.append((lTMP, c))
            lTMP -= 1
        if (lTMP != -1 and self.cases[lTMP][c].couleur != p.couleur):
            resultList.append((lTMP, c))

        cTMP = c + 1
        while (cTMP != 8 and self.cases[l][cTMP] == False):
            resultList.append((l, cTMP))
            cTMP += 1
        if (cTMP != 8 and self.cases[l][cTMP].couleur != p.couleur):
            resultList.append((l, cTMP))

        cTMP = c - 1
        while (cTMP != -1 and self.cases[l][cTMP] == False):
            resultList.append((l, cTMP))
            cTMP -= 1
        if (cTMP != -1 and self.cases[l][cTMP].couleur != p.couleur):
            resultList.append((l, cTMP))

        return resultList

    def visionCavalier(self, l, c, p):
        resultList = []
        for lTMP in [2, -2, -1, 1]:
            if (lTMP == 2 or lTMP == -2):
                for cTMP in [-1, 1]:
                    cTMP += c
                    if ((lTMP + l) < 8 and (lTMP + l) > -1 and cTMP < 8 and cTMP > -1):
                        if (self.cases[lTMP + l][cTMP] == False):
                            resultList.append(((lTMP + l), cTMP))
                        elif (self.cases[lTMP + l][cTMP].couleur != p.couleur):
                            resultList.append(((lTMP + l), cTMP))
            else:
                for cTMP in [-2, 2]:
                    cTMP += c
                    if ((lTMP + l) < 8 and (lTMP + l) > -1 and cTMP < 8 and cTMP > -1):
                        if (self.cases[lTMP + l][cTMP] == False):
                            resultList.append(((lTMP + l), cTMP))
                        elif (self.cases[lTMP + l][cTMP].couleur != p.couleur):
                            resultList.append(((lTMP + l), cTMP))

        return resultList

    def visionPion(self, l, c, p):
        resultList = []

        # m permet de savoir dans quelle direction le point avance sur le plateau
        if (self.couleurHaut == "Blanc"):
            if (self.cases[l][c].couleur != "Blanc"):
                m = -1
            else:
                m = 1
        else:
            if (self.cases[l][c].couleur != "Blanc"):
                m = 1
            else:
                m = -1

        # Etat 1 du piont : peut avancer de 2 case
        if (self.cases[l][c].etat == 1):
            i = 1
            while (self.cases[l + (i * m)][c] == False and i < 3):
                resultList.append((l + (i * m), c))
                i += 1
        else:
            # Etat 0 ou 2 du piont : peut avancer de 1 case
            if -1<(l+(1*m)) and (l+(1*m))<8:
                if (self.cases[l + (1 * m)][c] == False):
                    resultList.append(((l + (1 * m), c)))

        # Peut importe l'état, on regarde si une prise peut étre envisagée
        lTMP = l + (1 * m)
        for i in [1, -1]:
            if (-1 < c + i and c + i < 8 and -1 < lTMP and lTMP < 8):
                if (self.cases[lTMP][c + i] != False and self.cases[lTMP][c + i].couleur != self.cases[l][
                    c].couleur):
                    resultList.append(((lTMP, c + i)))

        # Etat 2 on regarde si une prise en passant peut étre envisagée
        for i in [1, -1]:
            if (-1 < c + i and c + i < 8):
                pTMP = self.cases[l][c + i]
                if (pTMP != False and pTMP.couleur != self.cases[l][c].couleur and pTMP.etat == 2 and
                        self.cases[l + m][c + i] == False):
                    resultList.append(((l + m, c + i)))

        return resultList

    # Fonction à optimiser
    def visionRoi(self, l, c, p):
        resultList = []
        # Etat 1 du Roi : ROC possible
        if (self.cases[l][c].etat == 1):
            flag = True
            if (self.cases[l][c].couleur == self.couleurJ):
                # Grand ROC
                for i in range(1, 4):
                    if (self.cases[7][i] != False):
                        flag = False
                if (flag and self.cases[7][0] != False and self.cases[7][
                    0].etat == 1):  # Etat 1 de la Tour : ROC possible
                    resultList.append((7, 2))

                flag = True
                # Peit ROC
                for i in range(5, 7):
                    if (self.cases[7][i] != False):
                        flag = False
                if (flag and self.cases[7][7] != False and self.cases[7][7].etat == 1):
                    resultList.append((7, 6))

            else:
                for i in range(1, 4):
                    if (self.cases[0][i] != False):
                        flag = False
                if (flag and self.cases[0][0] != False and self.cases[0][0].etat == 1):
                    resultList.append((0, 2))
                flag = True
                for i in range(5, 7):
                    if (self.cases[0][i] != False):
                        flag = False
                if (flag and self.cases[0][7] != False and self.cases[0][7].etat == 1):
                    resultList.append((0, 6))

        for lTMP in [l - 1, l, l + 1]:
            for cTMP in [c - 1, c, c + 1]:
                if ((lTMP < 8 and lTMP > -1) and (cTMP < 8 and cTMP > -1)):
                    if (self.cases[lTMP][cTMP] == False):
                        resultList.append((lTMP, cTMP))
                    elif (self.cases[lTMP][cTMP].couleur != self.cases[l][c].couleur):
                        resultList.append((lTMP, cTMP))

        return resultList

    def visionPossibilte(self, l, c):
        resultList = []
        if (self.cases[l][c] == False):
            return False

        pieceSelectionnee = self.cases[l][c]

        if (pieceSelectionnee.nom == "tour"):
            return self.visionLigne(l, c, pieceSelectionnee)

        elif (pieceSelectionnee.nom == "fou"):
            return self.visionDiagonale(l, c, pieceSelectionnee)

        elif (pieceSelectionnee.nom == "dame"):
            resultList += self.visionLigne(l, c, pieceSelectionnee)
            resultList += self.visionDiagonale(l, c, pieceSelectionnee)
            return resultList

        elif (pieceSelectionnee.nom == "cavalier"):
            resultList += self.visionCavalier(l, c, pieceSelectionnee)
            return resultList

        elif (pieceSelectionnee.nom == "pion"):
            resultList += self.visionPion(l, c, pieceSelectionnee)
            return resultList

        elif (pieceSelectionnee.nom == "roi"):
            resultList += self.visionRoi(l, c, pieceSelectionnee)
            return resultList

        return resultList

    def getPosRoi(self, couleur):
        for l in range(0, 8):
            for c in range(0, 8):
                tmp = self.cases[l][c]
                if (tmp != False and tmp.nom == "roi" and tmp.couleur == couleur):
                    return (l, c)
        return False

    #Vérifie si le roi de la couleur donner est en echec ou non
    def verifEchec(self, couleur):
        posRoi = self.getPosRoi(couleur)
        listeCoupAdversaire = []

        if (couleur == "Blanc"):
            autreCouleur = "Noir"
        else:
            autreCouleur = "Blanc"

        if (posRoi == False):
            return False

        for l in range(0, 8):
            for c in range(0, 8):
                tmp = self.cases[l][c]
                if (tmp != False and tmp.couleur == autreCouleur):
                    listeTMP = self.visionPossibilte(l, c)
                    for i in listeTMP:
                        listeCoupAdversaire.append(i)

        nb = listeCoupAdversaire.count(posRoi)

        if (nb == 0):
            return False

        return True
        # return listeCoupAdversaire

    #Retourne la liste de tous les coups possible d'une couleur donner sans vérifier si ce sont des coups légaux 
    def getListeCoupPossible(self, couleur):
        listeCoupNecessaire = []
        for l in range(0, 8):
            for c in range(0, 8):
                p = self.cases[l][c]
                if (p != False and p.couleur == couleur and p.nom!="roi"):
                    listeTMP = self.visionPossibilte(l, c)
                    for i in listeTMP:

                        self.cases[l][c] = False
                        pTMP = self.cases[i[0]][i[1]]
                        self.cases[i[0]][i[1]] = p

                        if (not self.verifEchec(couleur)):
                            listeCoupNecessaire.append(i)

                        self.cases[l][c] = p
                        self.cases[i[0]][i[1]] = pTMP

        return listeCoupNecessaire

    #Retourne la liste de tous les coups possible du roi d'une couleur donner en vérifiant si ce sont des coups légaux 
    def getListeCoupNecessaireRoi(self,couleur):
        posRoi=self.getPosRoi(couleur)
        roi=self.cases[posRoi[0]][posRoi[1]]
        listeTMP=self.visionPossibilte(posRoi[0],posRoi[1])
        listeCoupNecessaireRoi=[]

        for i in listeTMP:
            
            self.cases[posRoi[0]][posRoi[1]]=False
            pTMP=self.cases[i[0]][i[1]]
            self.cases[i[0]][i[1]]=roi

            if(not self.verifEchec(couleur)):
                listeCoupNecessaireRoi.append(i)

            self.cases[posRoi[0]][posRoi[1]]=roi
            self.cases[i[0]][i[1]]=pTMP
        return listeCoupNecessaireRoi

    #Retourne la liste de tous les coups possible d'une pièce en vérifiant si ce sont des coups légaux garce aux coordonées 
    def getListeAnd(self, ligne, colonne):
        if(self.cases[ligne][colonne]==False):
            return False
        elif(self.cases[ligne][colonne].nom=="roi"):
            liste1=self.getListeCoupNecessaireRoi(self.cases[ligne][colonne].couleur)
        else:
            liste1=self.getListeCoupPossible(self.cases[ligne][colonne].couleur)

        liste2=self.visionPossibilte(ligne, colonne)
        listeTMP = []
        for i in liste1:
            if (i in liste2):
                listeTMP.append(i)
        return list(set(listeTMP))

    def plusDeCoupAJouer(self, couleur):
        liste = []
        liste = self.getListeCoupPossible(couleur)+self.getListeCoupNecessaireRoi(couleur)

        if (not liste):
            return True
        else:
            return False

    #Donne et change les états d'une pièce 
    def defEtat(self, ligne, colonne, nouvelleLigne, nouvelleColonne, pManger):
        p = self.cases[nouvelleLigne][nouvelleColonne]
        if (p != False and p.nom == "pion" and p.etat == 1):
            if (abs(ligne - nouvelleLigne) == 2):
                flag = False
                for i in [1, -1]:
                    if (-1 < nouvelleColonne + i and nouvelleColonne + i < 8):
                        if (self.cases[nouvelleLigne][nouvelleColonne + i] != False):
                            flag = True
                if (flag):
                    self.cases[nouvelleLigne][nouvelleColonne].etat = 2
                else:
                    self.cases[nouvelleLigne][nouvelleColonne].etat = 0
            else:
                self.cases[nouvelleLigne][nouvelleColonne].etat = 0

        if (p.nom == "pion" and pManger == False):
            # m permet de savoir dans quelle direction le point avance sur le plateau
            if (self.couleurHaut == "Blanc"):
                if (p.couleur != "Blanc"):
                    m = 1
                else:
                    m = -1
            else:
                if (p.couleur != "Blanc"):
                    m = -1
                else:
                    m = 1
            self.cases[nouvelleLigne + m][nouvelleColonne] = False

        if (p != False and p.nom == "tour" and p.etat == 1):
            self.cases[nouvelleLigne][nouvelleColonne].etat = 0
        elif (p != False and p.nom == "roi" and p.etat == 1):
            self.cases[nouvelleLigne][nouvelleColonne].etat = 0
            if (abs(colonne - nouvelleColonne) == 2):
                # Grand ROC
                if (nouvelleColonne == 2):
                    self.mouvementManuel(ligne, 0, ligne, 3)
                    self.cases[ligne][3].etat = 0
                # Petit ROC
                elif (nouvelleColonne == 6):
                    self.mouvementManuel(ligne, 7, ligne, 5)
                    self.cases[ligne][5].etat = 0

    def defEtatPion(self, couleur):
        for l in range(0, 8):
            for c in range(0, 8):
                pTMP = self.cases[l][c]
                if (pTMP != False and pTMP.couleur == couleur and pTMP.nom == "pion" and pTMP.etat == 2):
                    self.cases[l][c].etat = 0

    def partieFinie(self):
        if (self.plusDeCoupAJouer("Noir") and self.verifEchec("Noir")):  # 1 : Victoire B
            return 1
        elif (self.plusDeCoupAJouer("Blanc") and self.verifEchec("Blanc")):  # 2 : Victoire N
            return 2
        elif (self.plusDeCoupAJouer("Blanc") or (self.plusDeCoupAJouer("Noir"))):  # 3 : Match nul
            return 3
        else:  # 0 : La partie continue
            return 0

    def liste_piece_mange(self, p):
        cptT, cptF, cptC = 1, 1, 1
        pm = p
        if self.pieces_mangees:
            for i in self.pieces_mangees:
                # print(f"T : {cptT}, F : {cptF}, C : {cptC}")
                if i.couleur == p.couleur:
                    if i.nom == "dame" and p.nom == "dame":
                        pm = piece("pion", p.couleur)
                    elif i.nom == "tour" and p.nom == "tour":
                        if cptT < 2:
                            cptT += 1
                        else:
                            pm = piece("pion", p.couleur)
                    elif i.nom == "fou" and p.nom == "fou":
                        if cptF < 2:
                            cptF += 1
                        else:
                            pm = piece("pion", p.couleur)
                    elif i.nom == "cavalier" and p.nom == "cavalier":
                        if cptC < 2:
                            cptC += 1
                        else:
                            pm = piece("pion", p.couleur)
        self.pieces_mangees.append(pm)        

    # return | 0 : case vide | 1 : pas de soucis | 2 : pièce clouée | 3 : choix de mouvement invalide
    def mouvement(self, ligne, colonne, nouvelleLigne, nouvelleColonne):
        if (self.cases[ligne][colonne] == False):
            return 0
        else:
            listePossibilite = self.getListeAnd(ligne,colonne)
            if ((nouvelleLigne, nouvelleColonne) in listePossibilite):
                p = self.cases[ligne][colonne]
                pManger = self.cases[nouvelleLigne][nouvelleColonne]

                self.cases[ligne][colonne] = False
                self.cases[nouvelleLigne][nouvelleColonne] = p

                if (not self.verifEchec(p.couleur)):
                    p.posY, p.posX = nouvelleLigne, nouvelleColonne
                    if p.nom == "pion" and (p.posY == 0 or p.posY == 7):
                        p = self.promotion(p)
                    self.cases[nouvelleLigne][nouvelleColonne] = p
                    self.defEtat(ligne, colonne, nouvelleLigne, nouvelleColonne, pManger)
                    self.joue += 1
                    if pManger:
                        self.liste_piece_mange(pManger)

                    return 1
                else:
                    self.cases[ligne][colonne] = p
                    self.cases[nouvelleLigne][nouvelleColonne] = pManger
                    return 2
            else:
                return 3

    # Algo Aléatoire
    def jeuOrdi(self):
        couleur = self.couleurHaut
        listePiece = []
        for l in range(0, 8):
            for c in range(0, 8):
                if (self.cases[l][c] != False and self.cases[l][c].couleur==couleur):
                    listePiece.append((l, c))
        while (True):

            nbRand = random.randint(0, len(listePiece)-1)
            coo = listePiece[nbRand]

            listeCoup = []
            listeCoup = self.getListeAnd(coo[0], coo[1])

            if (len(listeCoup) != 0):
                break
        nbRand = random.randint(0, len(listeCoup)-1)
        coo2 = listeCoup[nbRand]
        time.sleep(1)
        self.mouvement(coo[0], coo[1], coo2[0], coo2[1])

    # Algo Min Max
    def JeuMinMax(self):
        ilegal=[]
        while(True):
            listeTMP=[]
            for l in range(0,8):
                for c in range(0,8):
                    if(self.cases[l][c]!=False):
                        listeTMP.append((self.cases[l][c].nom,self.cases[l][c].couleur,c,l,self.cases[l][c].decalX,self.cases[l][c].decalY,self.cases[l][c].etat))
                    else:
                        listeTMP.append(("F","F",c,l))
            with open("minmax/saveP.json","w") as f:
                json.dump(listeTMP,f)
            with open("minmax/saveC.json","w") as f:
                json.dump(self.couleurJ,f)
            with open("minmax/saveD.json","w") as f:
                json.dump(self.J.difficulter,f)

            p=plateauMinMax(self.couleurJ,self.cases)
            resultat=p.best_move(2,ilegal)

            try:
                with open("minmax/saveP.json","r") as rf:
                    listeTMP=json.load(rf)
                    for caseTMP in listeTMP:
                        if(caseTMP[0]=="F"):
                            self.cases[caseTMP[3]][caseTMP[2]]=False
                        else:
                            self.cases[caseTMP[3]][caseTMP[2]]=piece(caseTMP[0],caseTMP[1],caseTMP[2],caseTMP[3],caseTMP[4],caseTMP[5],caseTMP[6])
                with open("minmax/saveC.json","r") as rf:
                    coul=json.load(rf)  
                    self.joue=1 if coul=="Blanc" else 0
                with open("minmax/saveD.json","r") as rf:
                    self.J.difficulter=json.load(rf)  


            except:
                print("Erreur pas de sauvegarde")

            if((resultat==None) and ((resultat[2], resultat[3]) not in self.getListeAnd(resultat[0],resultat[1]))):
                ilegal.append(resultat)
                print("ILEGAL")
                print(ilegal)
                print("______")
            else:
                break
        if(resultat!=None):
            self.mouvement(resultat[0],resultat[1],resultat[2],resultat[3])
        print(resultat)

    def draw_plateau(self):
        for column in range(8):
            for row in range(8):
                rect = pygame.Rect(column * self.tailleCase + self.decalX, row * self.tailleCase + self.decalY, self.tailleCase, self.tailleCase)
                couleur = "#E7E4E2" if (row + column) % 2 == 0 else "#67A032"
                pygame.draw.rect(self.screen, couleur, rect)

    def draw_piece(self):
        for column in range(8):
            for row in range(8):
                if self.cases[row][column]:
                    image = self.cases[row][column]
                    self.screen.blit(image.img, (image.posX * 80 + image.decalX, image.posY * 80 + image.decalY))

    def draw_mouvement(self):
        p = self.isSelect()

        if p:
            mvt = self.getListeAnd(p.posY, p.posX)
            for col in range(0, 8):
                for row in range(0, 8):
                    if (row, col) in mvt:
                        pX = col * 80 + self.decalX + 40
                        pY = row * 80 + self.decalY + 40
                        # print(f"DP----{p.posX}-{p.posY}")
                        pygame.draw.circle(self.screen, "red", (pX, pY), 10, 0)

    def draw_select(self):
        p = self.isSelect()
        if p:
            # print("rond")
            pX = p.posX * 80 + p.decalX + 40
            pY = p.posY * 80 + p.decalY + 40
            # print(f"DP----{p.posX}-{p.posY}")
            pygame.draw.circle(self.screen, "#262421", (pX, pY), 20, 4)
    
    def draw_piecesM(self):
        cptJ, cptO = 0, 0
        new_taille = 30

        xJ, yJ = self.decalX * 2 + 100, 630
        xO, yO = self.decalX / 3 - 80, 160

        for i in self.pieces_mangees:
            if i.couleur != self.couleurJ:
                cptJ += 1
                if cptJ > 8:
                    i.decalY = yJ - 38
                else:
                    i.decalY = yJ
                i.decalX, i.taille = (cptJ % 9) * 35 + xJ, new_taille
            else:
                cptO += 1
                if cptO > 8:
                    i.decalY = yO + 38
                else:
                    i.decalY = yO
                i.decalX, i.taille = (cptO % 9) * 35 + xO, new_taille

            self.screen.blit(i.img, (i.decalX, i.decalY))

    def draw(self):
        self.draw_plateau()
        self.draw_piece()
        self.draw_select()
        self.draw_mouvement()
        self.draw_piecesM()
        pygame.display.update()

    #boucle de jeu
    def game(self,save=0):
        abandon=0
        run = True
        if(save==1):
            try:
                with open("saves/saveC.json","r") as rf:
                    coul=json.load(rf)
                    self.joue=0 if coul=="Blanc" else 1
                with open("saves/saveD.json","r") as rf:
                    self.J.difficulter=json.load(rf)
                with open("saves/saveP.json","r") as rf:
                    listeTMP=json.load(rf)
                    for caseTMP in listeTMP:
                        if(caseTMP[0]=="F"):
                            self.cases[caseTMP[3]][caseTMP[2]]=False
                        else:
                            self.cases[caseTMP[3]][caseTMP[2]]=piece(caseTMP[0],caseTMP[1],caseTMP[2],caseTMP[3],caseTMP[4],caseTMP[5],caseTMP[6])
                with open("saves/saveM.json","r") as rf:
                    listeM=json.load(rf)
                    for i in listeM:
                        self.pieces_mangees.append(piece(i[0], i[1]))
            except:
                print("Erreur pas de sauvegarde")
                self.J.difficulter="facile"
            finally:
                pass

        ma_police = pygame.font.Font(None, 70)
        txt_ordi = ma_police.render("Joueur2", True, (255, 255, 255))
        txt_joueur = ma_police.render("Joueur1", True, (255, 255, 255))
        self.screen.blit(txt_ordi, (self.decalX / 3, 100))
        self.screen.blit(txt_joueur, (self.decalX * 2 + 200, 700))

        while self.partieFinie() == 0 and run:
            self.draw()

            self.boutonQuit.draw_button()

            coul = "Blanc" if self.joue % 2 == 0 else "Noir"

            self.defEtatPion(coul)

            if self.couleurJ == coul or self.J.difficulter=="joueur":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            x, y = event.pos

                            if self.boutonQuit.estClick(event.pos):
                                listeTMP=[]
                                for l in range(0,8):
                                    for c in range(0,8):
                                        if(self.cases[l][c]!=False):
                                            listeTMP.append((self.cases[l][c].nom,self.cases[l][c].couleur,c,l,self.cases[l][c].decalX,self.cases[l][c].decalY,self.cases[l][c].etat))
                                        else:
                                            listeTMP.append(("F","F",c,l))
                                liteM = []
                                for i in self.pieces_mangees:
                                    liteM.append((i.nom, i.couleur))

                                with open("saves/saveP.json","w") as f:
                                    json.dump(listeTMP,f)
                                with open("saves/saveC.json","w") as f:
                                    json.dump(coul,f)
                                with open("saves/saveD.json","w") as f:
                                    json.dump(self.J.difficulter,f)
                                with open("saves/saveM.json", "w") as f:
                                    json.dump(liteM, f)                                
                                root_qst = tk.Tk()
                                root_qst.withdraw()
                                quitter = messagebox.askquestion("Quitter la partie", "Êtes-vous sûr de vouloir quitter ?\n La partie sera sauvegardé")
                                root_qst.destroy()
                                if quitter == "yes":
                                    run = False
                                    abandon = 1

                            if (x >= self.decalX and y >= self.decalY) and (x <= self.decalX + 8 * 80 and y <= self.decalY + 8 * 80):
                                x -= self.decalX
                                y -= self.decalY
                                col = int(x // 80)
                                row = int(y // 80)

                                if self.isSelect():
                                    if self.cases[row][col] and self.bon_joueur(self.cases[row][col]):
                                        self.select(self.cases[row][col])

                                    else:
                                        p = self.isSelect()
                                        self.mouvement(p.posY, p.posX, row, col)
                                        self.unselect(p)

                                else:
                                    if(-1<row and -1<col and 8>row and 8>col):
                                        if self.cases[row][col] and self.bon_joueur(self.cases[row][col]):
                                            self.select(self.cases[row][col])
            else:
                if(self.J.difficulter=="difficile"):
                    self.JeuMinMax()
                if(self.J.difficulter=="facile"):
                    self.jeuOrdi()
                self.draw()

                
        if not abandon:
            if self.partieFinie() == 1:
                txt = "Joueur1 a gagné !" if self.couleurJ == "Blanc" else "Joueur2 a gagné !"
            elif self.partieFinie() == 2:
                txt = "Joueur1 a gagné !" if self.couleurJ == "Noir" else "Joueur2 a gagné !"
            else:
                txt = "Match nul !"
            if(os.path.exists("saves/saveP.json") and os.path.exists("saves/saveC.json")):
                os.remove("saves/saveP.json")
                os.remove("saves/saveC.json")
                os.remove("saves/saveD.json")

            txt = txt + "\nVoulez-vous rejouer ?"
        else:
            txt = "Retourner au menu principal ?"
        
        if(self.partieFinie()!=0):
            if self.partieFinie() == 1:
                txt = "Vous avez gagné !" if self.couleurJ == "Blanc" else "Vous avez perdu !"
            elif self.partieFinie() == 2:
                txt = "Vous avez gagné !" if self.couleurJ == "Noir" else "Vous avez perdu !"
            else:
                txt = "Match nul !"

            if(os.path.exists("saves/saveP.json") and os.path.exists("saves/saveC.json")):
                os.remove("saves/saveP.json")
                os.remove("saves/saveC.json")
                os.remove("saves/saveD.json")

        txt = txt + "\nVoulez-vous rejouer ?"

        root_qst = tk.Tk()
        root_qst.withdraw()
        fin = messagebox.askquestion("Fin de partie", txt)
        root_qst.destroy()

        return 1
