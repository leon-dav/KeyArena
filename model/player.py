import pygame
import math
import random
from pygame.surface import Surface
from model.keyBoardManager import KeyBoardManager
from collision import Circle, Vector
import config

v = Vector


class Player:
    """
    Represents a player character in the game.

    Attributes:
        x (int): The x-coordinate of the player's position.
        y (int): The y-coordinate of the player's position.
        team (int): The team the player belongs to.
        key (str): The key used to control the player.
        collision_area (Circle): The collision area of the player.
        mass (float): The mass of the player.
        color (tuple): The color of the player.
        vx (float): The velocity on the x-axis.
        vy (float): The velocity on the y-axis.
        current_direction (float): The current direction of the player's barrel.
        title_text (Surface): The text representing the player's key.
        title_rect (Rect): The rectangle containing the text.
        positions (list): List of positions for the barrel direction.
    """

    def __init__(self, x: int, y: int, team: int, key: str) -> None:
        """Initializes a player.

        Args:
            x (int): The x-coordinate of the player's position.
            y (int): The y-coordinate of the player's position.
            team (int): The team the player belongs to.
            key (str): The key used to control the player.
        """

        self.x = x
        self.y = y
        self.team = team
        self.key = key

        myfont = pygame.font.SysFont("Comic Sans MS", 30)

        self.title_text = myfont.render(self.key, True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(self.x, self.y))

        self.collision_area = Circle(v(x, y), config.PLAYER_RADIUS)
        self.mass = 1
        self.color = config.TEAM_TWO_COLOR if self.team else config.TEAM_ONE_COLOR
        self.vx = 0
        self.vy = 0
        self.current_direction = random.uniform(0, 2 * math.pi)

        # generate direction line positions
        self.positions = []
        t = 0
        while t < 2 * math.pi:
            self.positions.append(
                (
                    config.PLAYER_BARREL_LENGTH * math.cos(t) + self.x,
                    config.PLAYER_BARREL_LENGTH * math.sin(t) + self.y,
                )
            )
            t += 0.03

    def update(self, keyBoardManager: KeyBoardManager, elapsed: float) -> None:
        """
        Update the player's position based on keyboard input.

        Args:
            keyBoardManager (KeyBoardManager): The keyboard manager for input handling.
            elapsed (float): The elapsed time since the last update.
        """

        if keyBoardManager and self.key in keyBoardManager.keys:
            self.vx += math.cos(self.current_direction) * config.PLAYER_SPEED
            self.vy += math.sin(self.current_direction) * config.PLAYER_SPEED
            keyBoardManager.keys.remove(
                self.key
            )  # remove entry to not move several time

        # slow down speed by simulating a ground friction
        self.vx *= 1 / (1 + (elapsed / 1000 * config.GROUND_DRAG))
        self.vy *= 1 / (1 + (elapsed / 1000 * config.GROUND_DRAG))

        # update position
        self.x += self.vx * elapsed / 1000
        self.y += self.vy * elapsed / 1000

        self.collision_area.pos = v(self.x, self.y)

        # update barrel angle
        self.current_direction += config.PLAYER_BARREL_ROTATION_SPEED * elapsed / 1000
        if self.current_direction >= 2 * math.pi:
            self.current_direction = 0

        self.title_rect = self.title_text.get_rect(center=(self.x, self.y))

    def draw(self, screen: Surface) -> None:
        """
        Draw the player on the screen.

        Args:
            screen (Surface): The pygame surface to draw on.
        """

        # compute barrel shape + draw barrel
        dir_x = config.PLAYER_BARREL_LENGTH * math.cos(self.current_direction) + self.x
        dir_y = config.PLAYER_BARREL_LENGTH * math.sin(self.current_direction) + self.y

        center_L1 = ((dir_x + self.x) / 2, (dir_y + self.y) / 2)
        length = config.PLAYER_BARREL_LENGTH
        thickness = 5
        angle = math.atan2(self.y - dir_y, self.x - dir_x)

        UL = (
            center_L1[0]
            + (length / 2.0) * math.cos(angle)
            - (thickness / 2.0) * math.sin(angle),
            center_L1[1]
            + (thickness / 2.0) * math.cos(angle)
            + (length / 2.0) * math.sin(angle),
        )
        UR = (
            center_L1[0]
            - (length / 2.0) * math.cos(angle)
            - (thickness / 2.0) * math.sin(angle),
            center_L1[1]
            + (thickness / 2.0) * math.cos(angle)
            - (length / 2.0) * math.sin(angle),
        )
        BL = (
            center_L1[0]
            + (length / 2.0) * math.cos(angle)
            + (thickness / 2.0) * math.sin(angle),
            center_L1[1]
            - (thickness / 2.0) * math.cos(angle)
            + (length / 2.0) * math.sin(angle),
        )
        BR = (
            center_L1[0]
            - (length / 2.0) * math.cos(angle)
            + (thickness / 2.0) * math.sin(angle),
            center_L1[1]
            - (thickness / 2.0) * math.cos(angle)
            - (length / 2.0) * math.sin(angle),
        )

        # draw barrel
        pygame.draw.polygon(screen, (0, 0, 0), (UL, UR, BR, BL))

        # draw body circle
        pygame.draw.circle(screen, self.color, (self.x, self.y), config.PLAYER_RADIUS)

        # draw letter on top of the vessel
        screen.blit(self.title_text, self.title_rect)
