# faire une classe extends de menu avec une methode pour quitter
import pygame

from button import button

class menu(button):
    def __init__(self, txt, posX, posY, long, haut, screen):
        super().__init__(txt, posX, posY, long, haut, screen)


    # def action(self):
    #

pygame.init()
menu = menu("text")
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
