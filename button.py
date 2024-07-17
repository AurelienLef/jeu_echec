import pygame

class button:
    def __init__(self, txt, posX, posY, long, haut, screen):
        self.texte = txt
        self.posX = posX
        self.posY = posY
        self.long = long
        self.haut = haut
        self.screen = screen

    def draw_button(self):
        rect = pygame.Rect(self.posX, self.posY, self.long, self.haut)
        pygame.draw.rect(self.screen, "white", rect)
        txt = pygame.font.Font(None, 30)
        texte = txt.render("Quitter la partie", True, "black")
        texte_rect = texte.get_rect()
        texte_rect.center = (self.posX + self.long // 2, self.posY + self.haut // 2)
        self.screen.blit(texte, texte_rect)
        pygame.display.update()

    def estClick(self, pos):
        x, y = pos

        if (self.posX <= x <= self.posX + self.long) and (self.posY <= y <= self.posY + self.haut):
            return 1
        return 0

# pygame.init()
#
# screen = pygame.display.set_mode((0, 0))
# screen.fill(color="#262421")
#
# button = button("", 1173, 30, 200, 70, screen)
#
# run = True
# while run:
#     button.draw_button()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#         if event.type == pygame.MOUSEBUTTONUP:
#             if event.button == 1:
#                 print(button.estClick(event.pos))
#
# pygame.quit()