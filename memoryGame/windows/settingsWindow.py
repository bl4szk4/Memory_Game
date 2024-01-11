import pygame.draw

from memoryGame.windows.Windows import Windows
from memoryGame.gameboard_structures.buttonGenerator import ButtonGenerator
from enums.colors import Colors


class SettingsWindow(Windows):
    """
    Class for settings window that inherits from Windows class

    Attributes
    ----------
    :arg button_easy: easy difficulty button
    :arg button_medium: medium difficulty button
    :arg button_hard: hard difficulty button
    :arg button_camera_position: button for camera calibration
    :arg background_color: the color of the background

    Parameters
    ----------
    :param screen: screen of application
    :param screen_w: width of the screen
    :param screen_h: height of the screen
    """
    def __init__(self, screen, screen_w, screen_h):
        super().__init__(screen, screen_w, screen_h)
        self.button_easy = ButtonGenerator(self.screen, (screen_w / 2, screen_h * 0.2),
                                           Colors.DARK_GREEN.value, Colors.GRAY.value,
                                           'ŁATWY', 'consolas', 72)
        self.button_medium = ButtonGenerator(self.screen, (screen_w / 2, screen_h * 0.4),
                                           Colors.DARK_GREEN.value, Colors.GRAY.value,
                                           'ŚREDNI', 'consolas', 72)
        self.button_hard = ButtonGenerator(self.screen, (screen_w / 2, screen_h * 0.6),
                                             Colors.DARK_GREEN.value, Colors.GRAY.value,
                                             'TRUDNY', 'consolas', 72)
        self. button_camera_position = ButtonGenerator(self.screen, (screen_w / 2, screen_h * 0.8),
                                             Colors.DARK_GREEN.value, Colors.GRAY.value,
                                             'KAMERA', 'consolas', 72)
        self.background_color = Colors.BLACK.value

    def settings_init(self):
        self.screen.fill(self.background_color)
        self.button_easy.draw_button()
        self.button_medium.draw_button()
        self.button_hard.draw_button()
        pygame.draw.rect(self.screen, Colors.ORANGE.value, pygame.Rect(self.screen_w * .1, self.screen_h * .1,
                                                                       self.screen_w * .8, self.screen_h * .6), 3)
        self.button_camera_position.draw_button()

    def update_buttons(self, mouse):
        self.button_easy.update_button(mouse)
        self.button_medium.update_button(mouse)
        self.button_hard.update_button(mouse)
        self.button_camera_position.update_button(mouse)

