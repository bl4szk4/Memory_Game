import pygame

from enums.colors import Colors
from utils.mouseDetection import mouse_detection


class ButtonGenerator:
    def __init__(self, screen, location: tuple, text_color: tuple, focus_color: tuple, text: str,
                 text_font: str, text_size: int):
        self.location = location
        self.text = text
        self.text_color = text_color
        self.text_color_focus = focus_color
        self.font = pygame.font.SysFont(text_font, text_size)
        self.surface = self.font.render(text, True, text_color)
        self.text_rect = self.surface.get_rect()
        self.text_rect.center = (self.location[0], self.location[1])
        self.screen = screen
        self.color = focus_color

    def draw_button(self):

        self.screen.blit(self.surface, self.text_rect)
        pygame.display.update()

    def update_button(self, mouse: tuple):
        if mouse_detection((self.text_rect.x, self.text_rect.y),
                           self.text_rect.size, mouse):

            self.surface = self.font.render(self.text, True, self.text_color_focus)

        else:
            self.surface = self.font.render(self.text, True, self.text_color)
        self.screen.blit(self.surface, self.text_rect)
        pygame.display.update()

    def on_focus(self, mouse: tuple) -> bool:
        return mouse_detection((self.text_rect.x, self.text_rect.y), self.text_rect.size, mouse)
