import pygame
from view.button import Button
import config
from pygame.surface import Surface
from model.keyBoardManager import KeyBoardManager

class Credit():
    def __init__(self):

        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
        
        self.text0 = pygame.font.SysFont('Comic Sans MS', 80).render('KeyArena', True, (255, 255, 255))
        self.text1 = myfont.render('Dive into intense multiplayer battles with friends on a single keyboard in this addictively competitive 2D game!', True, (255, 255, 255))
        self.text2 = myfont.render('Take command of your vessel, capture map territories, and conquer your opponents in this 2D geometric showdown.', True, (255, 255, 255))
        self.text3 = myfont.render('Are you up for the challenge?', True, (255, 255, 255))
        self.text4 = myfont.render('Developed by: Leon Davidovski', True, (255, 255, 255))
        self.text5 = myfont.render('All images generated with OpenAI DALL-E', True, (255, 255, 255))

        self.button_credit = Button(config.APPLICATION_WIDTH, config.APPLICATION_HEIGTH, "Back", 40, 'orange', 'bright_orange', 1/10, 9/10)
        self.button_exit = Button(config.APPLICATION_WIDTH, config.APPLICATION_HEIGTH, "Exit", 40, 'red', 'bright_red', 9/10, 9/10)

        IMAGE_background = pygame.image.load('assets/credit.jpg').convert_alpha()
        self.background = pygame.transform.scale(IMAGE_background, (config.APPLICATION_WIDTH, config.APPLICATION_HEIGTH))

        self.transition = None
    
    def update(self, keyBoardManager: KeyBoardManager, elapsed: float):
        self.button_credit.update(keyBoardManager, elapsed)
        self.button_exit.update(keyBoardManager, elapsed)
        
        if self.button_credit.click:
            self.transition = {'transition': 'welcome'}
        
        if self.button_exit.click:
            keyBoardManager.running = False
    
    def draw(self, screen: Surface):
        screen.blit(self.background, (0, 0))

        screen.blit(self.text0, (20, 20))
        screen.blit(self.text1, (50, 100))
        screen.blit(self.text2, (50, 150))
        screen.blit(self.text3, (50, 200))
        screen.blit(self.text4, (50, 500))
        screen.blit(self.text5, (50, 530))
        
        self.button_credit.draw(screen)
        
        self.button_exit.draw(screen)