
from curses import mouseinterval
from json import dump
import random
from piece import piece

class plateauMinMax:
    def __init__(self, couleurJ,cases):
        self.couleurJ = couleurJ
        self.couleurHaut = "Blanc" if self.couleurJ == "Noir" else "Noir"
        self.joue = 0
        self.cases = cases

    valeurs_pieces = {
        'pion': 5,
        'cavalier': 30,
        'fou': 33,
        'tour': 56,
        'dame': 100,
        'roi': 900
    }

    TABLE_PION = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [0, 0, 0, 25, 25, 0, 0, 0],
        [5, 5, 10, 30, 30, 10, 5, 5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    TABLE_CHEVALIER = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]

    TABLE_FOU = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ]
    
    TABLE_TOUR = [
        [0, -40, -20, 5, 5, -20, -40, 0],
        [-35, 0, 0, 0, 0, 0, 0, -35],
        [-15, 0, 0, 0, 0, 0, 0, -15],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    TABLE_DAME = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    TABLE_ROI = [
        [20, 30, 10, 0, 0, 10, 30, 20],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30]
    ]

    def recherche_piece(self, nom, couleur):
        for colonne in range(8):
            for ligne in range(8):
                if self.cases[ligne][colonne] and self.cases[ligne][colonne].nom == nom and self.cases[ligne][colonne].couleur == couleur:
                    return True
        return False

    def bon_joueur(self, p):
        if (self.joue % 2 == 0 and p.couleur == "Blanc") or (self.joue % 2 == 1 and p.couleur == "Noir"):
            return 1
        return 0

    def promotion(self, p):

        promo = ["dame", "tour", "fou", "cavalier"]
        promue = random.choice(promo)

        coul = "Blanc" if self.joue % 2 == 0 else "Noir"
        new_piece = piece(promue, coul, p.posX, p.posY)
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
                    if (self.cases[7][i] != False):        [20, 20, 0, 0, 0, 0, 20, 20],


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
    def getListeCoupNecessaireRoiMinMax(self,couleur):
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

    def getListeCoupPossibleSansEchec(self, couleur):
        listeCoupNecessaire = []
        for l in range(0, 8):
            for c in range(0, 8):
                p = self.cases[l][c]
                if (p != False and p.couleur == couleur):
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

    def getListeCoupPossibleMinMax(self, ligne, colonne):
        if(self.cases[ligne][colonne]==False):
            return False
        elif(self.cases[ligne][colonne].nom=="roi"):
            liste1=self.getListeCoupNecessaireRoiMinMax(self.cases[ligne][colonne].couleur)
        else:
            liste1=self.getListeCoupPossibleSansEchec(self.cases[ligne][colonne].couleur)
        liste2=self.visionPossibilte(ligne, colonne)
        listeTMP = []
        for i in liste1:
            if (i in liste2):
                listeTMP.append(i)
        
        return list(set(listeTMP))

    def plusDeCoupAJouer(self, couleur):
        liste = []
        liste = self.getListeCoupPossibleSansEchec(couleur)

        if (not liste):
            return True
        else:
            return False

    def defEtat(self, ligne, colonne, nouvelleLigne, nouvelleColonne, pManger):
        p = self.cases[nouvelleLigne][nouvelleColonne]
        if (p != False and p.nom == "pion" and p.etat == 1):
            p.etat = 0     
        if (p != False and p.nom == "tour" and p.etat == 1):
            self.cases[nouvelleLigne][nouvelleColonne].etat = 0
        elif (p != False and p.nom == "roi" and p.etat == 1):
            self.cases[nouvelleLigne][nouvelleColonne].etat = 0

    def defEtatPion(self, couleur):
        for l in range(0, 8):
            for c in range(0, 8):
                pTMP = self.cases[l][c]
                if (pTMP != False and pTMP.couleur == couleur and pTMP.nom == "pion" and pTMP.etat == 2):
                    self.cases[l][c].etat = 0
                if(pTMP != False and pTMP.nom == "roi"):
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

    # return | 0 : case vide | 1 : pas de soucis | 2 : pièce clouée | 3 : choix de mouvement invalide
    def mouvementMinMax(self, ligne, colonne, nouvelleLigne, nouvelleColonne):
        if (self.cases[ligne][colonne] == False):
            return 0
        else:
            listePossibilite = self.getListeCoupPossibleMinMax(ligne,colonne)
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
                    return 1
                else:
                    self.cases[ligne][colonne] = p
                    self.cases[nouvelleLigne][nouvelleColonne] = pManger
                    return 2
            else:
                return 3

######################### MIN MAX ######################################

    def evaluation(self):
        total_evaluation = 0
        for ligne in range(0, 8):
            for colonne in range(0, 8):
                piece = self.cases[ligne][colonne]
                if piece != False:
                    piece_value = self.valeurs_pieces[piece.nom]
                    piece_evaluation = 0

                    if piece.nom == 'pion':
                        piece_evaluation = self.TABLE_PION[ligne][colonne]
                    elif piece.nom == 'chevalier':
                        piece_evaluation = self.TABLE_CHEVALIER[ligne][colonne]
                    elif piece.nom == 'fou':
                        piece_evaluation = self.TABLE_FOU[ligne][colonne]
                    elif piece.nom == 'tour':
                        piece_evaluation = self.TABLE_TOUR[ligne][colonne]
                    elif piece.nom == 'dame':
                        piece_evaluation = self.TABLE_DAME[ligne][colonne]
                    elif piece.nom == 'roi':
                        piece_evaluation = self.TABLE_ROI[ligne][colonne]

                    if piece.couleur == self.couleurHaut:  # Pièces de l'IA
                        total_evaluation += piece_value + piece_evaluation
                    else:  # Pièces du joueur
                        total_evaluation -= piece_value + piece_evaluation
        return total_evaluation

    """    
    def evaluation(self):
        totalJ, totalO = 0, 0

        for row in range(8):
            for col in range(8):
                p = self.cases[row][col]

                if p:
                    # print(p.nom)
                    value = self.valeurs_pieces[p.nom]
                    # print(f"{p.nom} : {value} ->", end=' ')
                    liste = self.getListeAnd(row, col)
                    if liste:
                        value += len(liste)

                    if p.couleur == self.couleurJ:
                        totalJ += value
                    else:
                        totalO += value

        return totalO - totalJ
        """
        
    def minimax_alpha_beta(self, profondeur, alpha, beta, max,ilegal):
        if profondeur == 0 or self.partieFinie()!=0:
            return self.evaluation()
        if max:
            max_eval = float('-inf')
            for ligne in range(8):
                for colonne in range(8):
                    if (self.cases[ligne][colonne]!=False and self.cases[ligne][colonne].couleur==self.couleurHaut):
                        moves = self.getListeCoupPossibleMinMax(ligne, colonne)
                        for move in moves:
                            if(ilegal):
                                tmp=(ligne, colonne, move[0], move[1])
                                if(tmp in ilegal):
                                    break                            
                            p=self.mouvementMinMax(ligne, colonne, move[0], move[1])
                            if(p==1):
                                eval = self.minimax_alpha_beta( profondeur - 1, alpha, beta, False,ilegal)
                                self.mouvementManuel( move[0], move[1],ligne, colonne)
                                max_eval = max(max_eval, eval)
                                alpha = max(alpha, eval)
                                if (beta <= alpha):
                                    break
            return max_eval
        else:
            min_eval = float('inf')
            for ligne in range(8):
                for colonne in range(8):
                    if (self.cases[ligne][colonne]!=False and self.cases[ligne][colonne].couleur==self.couleurJ):
                        moves = self.getListeCoupPossibleMinMax(ligne, colonne)
                        for move in moves:
                            if(ilegal):
                                tmp=(ligne, colonne, move[0], move[1])
                                if(tmp in ilegal):
                                    break  
                            p=self.mouvementMinMax(ligne, colonne, move[0], move[1])
                            if(p==1):
                                eval = self.minimax_alpha_beta(profondeur - 1, alpha, beta, True,ilegal)
                                self.mouvementManuel( move[0], move[1],ligne, colonne)
                                min_eval = min(min_eval, eval)
                                beta = min(beta, eval)
                                if beta <= alpha:
                                    break
            return min_eval

    def best_move(self, profondeur,ilegal):
        
        max_eval = float('-inf')
        best_move = None
        for ligne in range(8):
            for colonne in range(8):
                if (self.cases[ligne][colonne]!=False and self.cases[ligne][colonne].couleur==self.couleurHaut):
                    moves = self.getListeCoupPossibleMinMax(ligne, colonne)
                    for move in moves:
                        if(ilegal):
                            tmp=(ligne, colonne, move[0], move[1])
                            if(tmp in ilegal):
                                break                              
                        p=self.mouvementMinMax(ligne, colonne, move[0], move[1])
                        if(p==1):
                            eval = self.minimax_alpha_beta(profondeur - 1, float('-inf'), float('inf'), False,ilegal)
                            self.mouvementManuel( move[0], move[1],ligne, colonne)
                            if eval > max_eval:
                                max_eval = eval
                                best_move = (ligne, colonne, move[0], move[1])
        return best_move
