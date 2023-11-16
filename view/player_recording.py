import pygame
from view.button import Button
import config
from model.player import Player
from pygame.surface import Surface
from model.keyBoardManager import KeyBoardManager

class Recording():
    """
    Represents the recording phase where players select their keys.
    """

    def __init__(self):

        self.myfont_large = pygame.font.SysFont('Comic Sans MS', 100)
        self.myfont_medium = pygame.font.SysFont('Comic Sans MS', 80)
        
        self.title_text = self.myfont_large.render('Select your key', True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(config.APPLICATION_WIDTH/2, config.APPLICATION_HEIGTH/8))

        self.button_start = Button(config.APPLICATION_WIDTH, config.APPLICATION_HEIGTH, "Start", 40, 'green', 'bright_green', 1/2, 9/10)

        self.teams_keys = {"BLUE": set(), "RED": set()}

        self.transition = None

        background_image = pygame.image.load('assets/selection.jpg').convert_alpha()
        self.background_image = pygame.transform.scale(background_image, (config.APPLICATION_WIDTH, config.APPLICATION_HEIGTH))

        self.players = []
    
    def update(self, keyBoardManager: KeyBoardManager, elapsed: float):
        """
        Update the recording phase.

        Args:
            keyBoardManager (KeyBoardManager): The keyboard manager.
            elapsed (float): The elapsed time since the last update.
        """

        self.button_start.update(keyBoardManager, elapsed)

        for event in keyBoardManager.events:
            if event.type == pygame.KEYDOWN:
                key = event.unicode
                if key not in self.teams_keys["BLUE"] and key not in self.teams_keys["RED"]:
                    if len(self.teams_keys["RED"]) < len(self.teams_keys["BLUE"]):
                        self.teams_keys["RED"].add(event.unicode)
                        self.players.append(Player(config.APPLICATION_WIDTH/4, 250 + 10*len(self.players), 1, event.unicode))
                    else:
                        self.teams_keys["BLUE"].add(event.unicode)
                        self.players.append(Player(config.APPLICATION_WIDTH/4*3, 250 + 10*len(self.players), 0, event.unicode))
        
        for r in self.players:
            r.update(keyBoardManager, elapsed)
    
    def draw(self, screen: Surface):
        """
        Draw the recording phase on the screen.

        Args:
            screen (Surface): The pygame surface to draw on.
        """

        screen.blit(self.background_image, (0, 0))
        
        screen.blit(self.title_text, self.title_rect)

        screen.blit(self.myfont_medium.render(str(len(self.teams_keys["BLUE"])) + " Players", True, (255, 255, 255)), (config.APPLICATION_WIDTH/7, config.APPLICATION_HEIGTH/6*5))
        screen.blit(self.myfont_medium.render(str(len(self.teams_keys["RED"])) + " Players", True, (255, 255, 255)), (config.APPLICATION_WIDTH/7*5, config.APPLICATION_HEIGTH/6*5))
        
        for r in self.players:
            r.draw(screen)
        

        self.button_start.draw(screen)
        if self.button_start.click:
            self.transition = {'transition': 'game', 'players': self.teams_keys}