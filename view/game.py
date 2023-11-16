import pygame
from levels.level import Level1
import config
from view.button import Button
from model.player import Player
from model.keyBoardManager import KeyBoardManager
from model.collisionSolver import CollisionSolver
from model.obstacle import Obstacle
from model.scorezone import ScoreZone
from pygame.surface import Surface

class Game:
    """
    Represents the game screen.

    Attributes:
        players (list): List of player objects.
        obstacles (list): List of obstacle objects.
        scorezones (list): List of scorezone objects.
        collisionSolver (CollisionSolver): The collision solver.
        transition: (Not defined in the code you provided)
        pause (bool): Flag to pause the game.
        scores (list): Scores of each team.
        myfont (Font): The font for displaying scores.
        i (int): (Not defined in the code you provided)
    """

    def __init__(self, teams_players: list = []):
        """
        Initializes the game.

        Args:
            teams_players (list): List of teams and players.
        """

        self.players = []
        for team_number, team in enumerate(teams_players):
            for index, key in enumerate(teams_players[team]):
                self.players.append(
                    Player(50 + 50 * team_number, 50 + 50 * index, team_number, key)
                )

        self.obstacles = []
        level = Level1()
        for obstacle in level.OBSTACLES:
            self.obstacles.append(Obstacle(obstacle["points"], obstacle["color"]))

        self.scorezones = []
        for scorezone in level.SCOREZONES:
            self.scorezones.append(ScoreZone(*scorezone))

        self.collisionSolver = CollisionSolver()

        self.transition = None

        self.pause = False

        # store score of each team
        self.scores = [0, 0]

        self.myfont = pygame.font.SysFont("Comic Sans MS", 40)

        self.button_back = Button(config.APPLICATION_WIDTH, config.APPLICATION_HEIGTH, "Back", 40, 'orange', 'bright_orange', 1/2, 9/10)

    def update(self, keyBoardManager: KeyBoardManager, elapsed: float) -> None:
        """
        Update the game state.

        Args:
            events: (Not defined in the code you provided)
            keyBoardManager (KeyBoardManager): The keyboard manager for input handling.
            elapsed (float): The elapsed time since the last update.
        """
        self.button_back.update(keyBoardManager, elapsed)
        if self.button_back.click:
            self.transition = {'transition': 'welcome'}

        if keyBoardManager.EchapClick:
            self.pause = not self.pause

        if not self.pause:
            # update everything
            for o in self.players:
                o.update(keyBoardManager, elapsed)
            for o in self.scorezones:
                o.update(self.players, elapsed)
                if o.current_inside_score == o.full_score:
                    self.scores[o.current_winning_team] += 0.01

            # solve collision
            self.collisionSolver.amend([*self.players, *self.obstacles])
    
    def draw_win(self, screen: Surface):
        self.pause = True

        if self.scores[0] > self.scores[1]:
            text = "The blues win!"
        elif self.scores[0] < self.scores[1]:
            text = "The reds win!"
        else:
            text = "No winner!"
        
        text = self.myfont.render(text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(config.APPLICATION_WIDTH / 2, config.APPLICATION_HEIGTH / 2))

        screen.blit(text, text_rect)
        self.button_back.draw(screen)

    def draw(self, screen: Surface) -> None:
        """
        Draw the game elements on the screen.

        Args:
            screen: The pygame surface to draw on.
        """

        # draw everything
        for player in self.players:
            player.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        for scorezone in self.scorezones:
            scorezone.draw(screen)

        # Display scores
        # score_text = f"{int(self.scores[0])} - {int(self.scores[1])}"
        score_blue = self.myfont.render(str(int(self.scores[0])), True, (0, 0, 255))
        score_blue_rect = score_blue.get_rect(center=(config.APPLICATION_WIDTH / 2 - 30, 20))

        text = self.myfont.render(" - ", True, (0, 0, 0))
        text_rect = text.get_rect(center=(config.APPLICATION_WIDTH / 2, 20))

        score_red = self.myfont.render(str(int(self.scores[1])), True, (255, 0, 0))
        score_red_rect = score_red.get_rect(center=(config.APPLICATION_WIDTH / 2 + 30, 20))

        screen.blit(score_blue, score_blue_rect)
        screen.blit(text, text_rect)
        screen.blit(score_red, score_red_rect)

        if self.scores[0] >= config.WINNING_SCORE or self.scores[1] >= config.WINNING_SCORE:
            self.draw_win(screen)
