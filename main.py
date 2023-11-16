"""
Project: KeyArena
Author: Leon Davidovski

Take command of your vessel, capture map territories, and conquer your opponents in this 2D geometric showdown.
"""

# ---------------------------------------------------------------------------------------------

import pygame
from model.keyBoardManager import KeyBoardManager
import config
from view.game import Game
from view.player_recording import Recording
from view.welcome import Welcome
from view.credit import Credit

# ---------------------------------------------------------------------------------------------

successes, failures = pygame.init()

if config.FULL_SCREEN:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    infoObject = pygame.display.Info()
    config.APPLICATION_WIDTH = infoObject.current_w
    config.APPLICATION_HEIGTH = infoObject.current_h
else:
    screen = pygame.display.set_mode(
        (config.APPLICATION_WIDTH, config.APPLICATION_HEIGTH)
    )

pygame.display.set_caption("KeyArena")
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

keyBoardManager = KeyBoardManager()

interface = Welcome()

# ---------------------------------------------------------------------------------------------

while keyBoardManager.running:
    # clean screen
    screen.fill((255, 255, 255))

    # control FPS
    elapsed = clock.tick(config.FPS)

    # screen transition
    if interface.transition and interface.transition["transition"] == "welcome":
        interface = Welcome()
    if interface.transition and interface.transition["transition"] == "game":
        interface = Game(interface.transition["players"])
    if interface.transition and interface.transition["transition"] == "credit":
        interface = Credit()
    if interface.transition and interface.transition["transition"] == "recording":
        interface = Recording()

    # get commands
    keyBoardManager.Arrow_callback(pygame.event.get())

    # update
    interface.update(keyBoardManager, elapsed)

    # draw
    interface.draw(screen)

    # pygame rendering
    pygame.display.update()