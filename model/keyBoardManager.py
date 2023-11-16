import pygame


class KeyBoardManager:
    def __init__(self):
        self.keys = set()

        self.mouseClick = False
        self.mouseUp = False

        self.EchapClick = False

        self.running = True

        self.events = None

    # gestion des touches : mise a jour des variables correspondantes
    def Arrow_callback(self, events):
        self.events = events
        self.mouseUp = False
        self.EchapClick = False
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keys.add(event.unicode)
            elif event.type == pygame.KEYUP:
                if event.unicode in self.keys:
                    self.keys.remove(event.unicode)
                if event.key == pygame.K_ESCAPE:
                    self.EchapClick = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseClick = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouseClick = False
                self.mouseUp = True
