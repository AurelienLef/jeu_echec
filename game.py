import pygame
from plateau import plateau
from joueur import joueur
from menus.accueil import accueil
from menus.menuPrincipal import menuPrincipal
from menus.menuMode import menuMode


ouv = accueil()
click = ouv.result_click()

if click == 1:
    while True:
        menu_p = menuPrincipal()
        jeu = menu_p.result_choix()
        if jeu == "jouer" or jeu == "continuer":
            chargerPartie=0
            if(jeu == "continuer"):
                chargerPartie=1
                mode=False
            else:
                menu_m = menuMode()
                mode = menu_m.result_choix()

                if mode[0] == "retour":
                    continue
                elif mode[2] == 1:
                    break

            pygame.init()
            screen1 = pygame.display.set_mode((0, 0))
            screen1.fill(color="#262421")

            screenInfo = pygame.display.Info()
            decalX = (screenInfo.current_w - 8 * 80) / 2
            decalY = (screenInfo.current_h - 8 * 80) / 4

            if(mode):
                j1 = joueur("Moi", mode[1],mode[0])
            else:
                j1 = joueur("Moi")

            plate = plateau("Plateau de jeu", 80, j1, screen1, decalX, decalY)

            new_part = plate.game(chargerPartie)
            print(new_part)
            pygame.quit()

            if new_part == "no":
                break
        elif jeu == "quitter":
            break

