import pygame.font
from memoryGame.gameboard_structures.buttonGenerator import ButtonGenerator
from enums.colors import Colors
from memoryGame.windows.Windows import Windows


class MenuWindows(Windows):
    """
    Class for main window that inherits from Windows class

    Attributes
    ----------
    :arg button_start: Start button instance
    :arg button_options: options button instance
    :arg background_color: the color of the background, defined as Black

    Parameters
    ----------
    :param screen: screen of application
    :param screen_w: width of the screen
    :param screen_h: height of the screen
    """
    def __init__(self, screen, screen_w, screen_h):
        super().__init__(screen, screen_w, screen_h)
        self.button_start = ButtonGenerator(self.screen, (screen_w / 2, screen_h * .25), Colors.DARK_GREEN.value,
                                            Colors.GRAY.value, "START", "consolas", 72)
        self.button_options = ButtonGenerator(screen, (screen_w / 2, screen_h * .5), Colors.DARK_GREEN.value,
                                              Colors.GRAY.value, "OPCJE", "consolas", 72)
        self.background_color = Colors.BLACK.value

    def menu_init(self):
        """
        Initializes the window
        """
        self.screen.fill(self.background_color)
        self.button_start.draw_button()
        self.button_options.draw_button()

    def update_buttons(self, mouse):
        """
        Highlights buttons when the mouse is above them
        :param mouse: position of the mouse
        """
        self.button_start.update_button(mouse)
        self.button_options.update_button(mouse)
