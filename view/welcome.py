import pygame
from view.button import Button
from pygame.surface import Surface
from model.keyBoardManager import KeyBoardManager
import config

class Welcome():
    def __init__(self):

        myfont = pygame.font.SysFont('Comic Sans MS', 250)
        self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
        
        self.title_text = myfont.render('KeyArena', True, (0, 0, 0))
        self.title_rect = self.title_text.get_rect(center=(config.APPLICATION_WIDTH/2, config.APPLICATION_HEIGTH/5))

        self.button_start = Button(config.APPLICATION_WIDTH, config.APPLICATION_HEIGTH, "Start", 40, 'green', 'bright_green', 1/10, 1/2)
        self.button_credit = Button(config.APPLICATION_WIDTH, config.APPLICATION_HEIGTH, "Credit", 40, 'orange', 'bright_orange', 9/10, 1/2)
        self.button_exit = Button(config.APPLICATION_WIDTH, config.APPLICATION_HEIGTH, "Exit", 40, 'red', 'bright_red', 9/10, 19/20)

        IMAGE_background = pygame.image.load('assets/welcome.jpg').convert_alpha()
        self.background = pygame.transform.scale(IMAGE_background, (config.APPLICATION_WIDTH, config.APPLICATION_HEIGTH))

        self.transition = None
    
    def update(self, keyBoardManager: KeyBoardManager, elapsed: float) -> None:
        self.button_start.update(keyBoardManager, elapsed)
        self.button_credit.update(keyBoardManager, elapsed)
        self.button_exit.update(keyBoardManager, elapsed)

        if self.button_start.click:
            self.transition = {'transition': 'recording'}
        
        if self.button_credit.click:
            self.transition = {'transition': 'credit'}
        
        if self.button_exit.click:
            keyBoardManager.running = False
    
    def draw(self, screen: Surface) -> None:
        screen.blit(self.background, (0, 0))

        screen.blit(self.title_text, self.title_rect)

        self.button_start.draw(screen)
        
        self.button_credit.draw(screen)
        
        self.button_exit.draw(screen)