import pygame

color_dict = {
    "red": (200, 0, 0),
    "green": (0, 200, 0),
    "orange": (200, 200, 0),
    "bright_red": (255, 0, 0),
    "bright_green": (0, 255, 0),
    "bright_orange": (255, 255, 0),
}


class Button:
    def __init__(
        self,
        window_width,
        window_height,
        text,
        policeSize,
        bg_color1,
        bg_color2,
        w_ratio,
        h_ratio,
        button_width=200,
        button_height=50,
    ):
        self.button_width = button_width
        self.button_height = button_height
        self.text = text

        myfont = pygame.font.SysFont("Comic Sans MS", policeSize)

        self.buttonCoord = [
            window_width * w_ratio - button_width / 2,
            window_height * h_ratio - button_height / 2,
            button_width,
            button_height,
        ]
        self.button_text = myfont.render(text, True, (255, 255, 255))
        self.button_rect = self.button_text.get_rect(
            center=(
                self.buttonCoord[0] + self.buttonCoord[2] / 2,
                self.buttonCoord[1] + self.buttonCoord[3] / 2,
            )
        )

        self.color = color_dict[bg_color1]
        self.bg_color1 = color_dict[bg_color1]
        self.bg_color2 = color_dict[bg_color2]
        self.click = False

    def update(self, keyBoardManager, elapsed: float):
        mouse = pygame.mouse.get_pos()
        self.click = False
        if (
            self.buttonCoord[0] < mouse[0] < self.buttonCoord[0] + self.buttonCoord[2]
            and self.buttonCoord[1]
            < mouse[1]
            < self.buttonCoord[1] + self.buttonCoord[3]
        ):
            self.color = self.bg_color2
            if keyBoardManager.mouseUp == True:
                self.click = True
        else:
            self.color = self.bg_color1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.buttonCoord)
        screen.blit(self.button_text, self.button_rect)
