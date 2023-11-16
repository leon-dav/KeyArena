import pygame
from collision import Poly, Vector
from pygame.surface import Surface

v = Vector


class Obstacle:
    # An obstacle in the World. Polygon define by points.

    def __init__(self, points: list, color: list) -> None:
        self.points = points
        self.color = color

        self.collision_area = Poly(v(0, 0), [v(a[0], a[1]) for a in points])

        self.vx = 0
        self.vy = 0

    def draw(self, screen: Surface) -> None:
        if self.color:
            pygame.draw.polygon(screen, self.color, self.points)
