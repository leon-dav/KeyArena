import pygame
import math
import pygame.gfxdraw
from collision import Circle, collide, Vector
from pygame.surface import Surface
import config

v = Vector


class ScoreZone:
    """
    Represents an area where players earn points when they are inside.

    Attributes:
        x (int): The x-coordinate of the center of the zone.
        y (int): The y-coordinate of the center of the zone.
        radius (int): The radius of the zone.
        parts (int): The number of sub-parts forming the circle.
        full_score (int): The time required to fully score in the zone.
        current_inside_score (int): The current score inside the zone.
        current_winning_team (int): The current winning team inside the zone.
        rotation_angle (float): The rotation angle for visual effects.
        positions (list): List of positions for sub-parts of the circle.
        colors (list): List of colors for sub-parts of the circle.
    """

    def __init__(
        self, x: int, y: int, radius: int, nb_parts: int = 20, score_time: int = 1000
    ) -> None:
        """
        Initializes a score zone.

        Args:
            x (int): The x-coordinate of the center of the zone.
            y (int): The y-coordinate of the center of the zone.
            radius (int): The radius of the zone.
            nb_parts (int): The number of sub-parts forming the circle.
            score_time (int): The time required to fully score in the zone.
        """

        self.x = x
        self.y = y
        self.radius = radius
        self.parts = nb_parts
        self.collision_zone = Circle(v(self.x, self.y), radius)  # the collision circle
        self.full_score = score_time
        self.current_inside_score = 0
        self.current_winning_team = 0
        self.rotation_angle = 0
        self.colors = [(0, 0, 0) for _ in range(self.parts)]

        self.initialize_positions_colors()

    def initialize_positions_colors(self):
        """
        Initialize positions and colors for sub-parts of the circle.
        """
        self.positions = []
        stepSize = 2 * math.pi / self.parts
        t = 0
        while t < 2 * math.pi:
            self.positions.append(
                (
                    self.radius * math.cos(t + self.rotation_angle) + self.x,
                    self.radius * math.sin(t + self.rotation_angle) + self.y,
                )
            )
            t += stepSize

    def update(self, players, elapsed: float) -> None:
        """
        Update the score zone based on player positions.

        Args:
            players (list): List of player objects.
            elapsed (float): The elapsed time since the last update.
        """

        for player in players:
            if collide(self.collision_zone, player.collision_area):
                if player.team == self.current_winning_team:
                    self.current_inside_score += 1
                else:
                    self.current_inside_score -= 1

                # control borders values
                if self.current_inside_score < 1:
                    self.current_inside_score = 1
                    self.current_winning_team = 1 - self.current_winning_team
                if self.current_inside_score > self.full_score:
                    self.current_inside_score = self.full_score

                # update circles color
                self.colors = [(0, 0, 0) for _ in self.colors]
                for pos in range(
                    int((self.current_inside_score / self.full_score * self.parts))
                ):
                    self.colors[pos] = (
                        config.TEAM_TWO_COLOR
                        if self.current_winning_team
                        else config.TEAM_ONE_COLOR
                    )

        self.rotation_angle += 0.001
        if self.rotation_angle >= 2 * math.pi:
            self.rotation_angle = 0

        self.initialize_positions_colors()

    def draw(self, screen: Surface) -> None:
        """
        Draw the score zone on the screen.

        Args:
            screen (Surface): The pygame surface to draw on.
        """
        for index, pos in enumerate(self.positions):
            pygame.draw.circle(screen, self.colors[index], pos, 7)
