import math
from collision import Vector, Response, collide
import pygame
from model.player import Player
from model.obstacle import Obstacle

v = Vector

class CollisionSolver:
    def __init__(self):
        pass

    def amend(self, objects):
        """
        Amend object velocities based on collisions.

        Args:
            objects (list): List of objects to check for collisions.
        """
        for index, obj1 in enumerate(objects):
            for obj2 in objects[index + 1 :]:
                self.handle_collision(obj1, obj2)

    def handle_collision(self, obj1, obj2):
        """
        Handle collision between two objects.

        Args:
            obj1: First object.
            obj2: Second object.
        """
        response = Response()
        if collide(obj1.collision_area, obj2.collision_area, response):
            if isinstance(obj1, Obstacle) and isinstance(obj2, Obstacle):
                pass
            elif isinstance(obj1, Player) and isinstance(obj2, Obstacle) or isinstance(obj2, Player) and isinstance(obj1, Obstacle):
                self.reflect_objects(obj1, obj2, response.overlap_n)
            else:
                self.elastic_collision(obj1, obj2, response.overlap_n)

    def reflect_objects(self, player, obstacle, overlap_n):
        """
        Reflect a player off an obstacle.

        Args:
            player (Player): Player object.
            obstacle (Obstacle): Obstacle object.
            overlap_n: Overlap normal vector.
        """
        velocity = pygame.math.Vector2(player.vx, player.vy).reflect(overlap_n)
        player.vx, player.vy = velocity.x, velocity.y

    def elastic_collision(self, obj1, obj2, overlap_n):
        """
        Handle elastic collision between two objects.

        Args:
            obj1: First object.
            obj2: Second object.
        """
        dx = obj1.x - obj2.x
        dy = obj1.y - obj2.y

        collision_angle = math.atan2(dy, dx)

        speed1 = math.sqrt(obj1.vx ** 2 + obj1.vy ** 2)
        speed2 = math.sqrt(obj2.vx ** 2 + obj2.vy ** 2)

        direction1 = math.atan2(obj1.vy, obj1.vx)
        direction2 = math.atan2(obj2.vy, obj2.vx)

        velocityx_1 = speed1 * math.cos(direction1 - collision_angle)
        velocityy_1 = speed1 * math.sin(direction1 - collision_angle)
        velocityx_2 = speed2 * math.cos(direction2 - collision_angle)
        velocityy_2 = speed2 * math.sin(direction2 - collision_angle)

        final_velocityx_1 = ((obj1.mass - obj2.mass) * velocityx_1 + (obj2.mass + obj2.mass) * velocityx_2) / (
                    obj1.mass + obj2.mass)
        final_velocityx_2 = ((obj1.mass + obj1.mass) * velocityx_1 + (obj2.mass - obj1.mass) * velocityx_2) / (
                    obj1.mass + obj2.mass)

        final_velocityy_1 = velocityy_1
        final_velocityy_2 = velocityy_2

        obj1.vx = math.cos(collision_angle) * final_velocityx_1 + math.cos(collision_angle + math.pi / 2) * final_velocityy_1
        obj1.vy = math.sin(collision_angle) * final_velocityx_1 + math.sin(collision_angle + math.pi / 2) * final_velocityy_1
        obj2.vx = math.cos(collision_angle) * final_velocityx_2 + math.cos(collision_angle + math.pi / 2) * final_velocityy_2
        obj2.vy = math.sin(collision_angle) * final_velocityx_2 + math.sin(collision_angle + math.pi / 2) * final_velocityy_2