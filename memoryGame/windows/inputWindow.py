import pygame.font
from enums.colors import Colors
from memoryGame.windows.Windows import Windows
from memoryGame.gameboard_structures.buttonGenerator import ButtonGenerator


class InputWindow(Windows):
    """
    Class for input window that inherits from Windows class

    Attributes
    ----------
    :arg user_input: string for username that is typed by a playet
    :arg font: font that is used for user input
    :arg button_ok: button instance for confirming username

    Parameters
    ----------
    :param screen: screen of application
    :param screen_w: width of the screen
    :param screen_h: height of the screen
    """

    def __init__(self, screen, screen_w, screen_h):
        super().__init__(screen, screen_w, screen_h)
        self.user_input = ''
        self.font = pygame.font.SysFont('consolas', int(self.screen_w / 15))
        self.button_ok = ButtonGenerator(screen, (self.screen_w / 2, self.screen_h * .75), Colors.DARK_GREEN.value,
                                             Colors.GRAY.value, "OK", "consolas", int(self.screen_w / 15))

    def input_init(self):
        """
        Initializes the window
        """
        self.screen.fill(Colors.BLACK.value)
        self.button_ok.draw_button()
        self.screen.fill(Colors.BLACK.value)
        surface_info = self.font.render("PODAJ NAZWĘ", True, Colors.DARK_GREEN.value)
        text_rect_info = surface_info.get_rect()
        text_rect_info.center = (self.screen_w / 2, self.screen_h * .25)
        self.screen.blit(surface_info, text_rect_info)
        pygame.display.update()

    def text_update(self, to_append: bool, letter=''):
        """
        Updates the username after pressing a key
        :param to_append: True if no backspace was pressed, False if backspace was pressed
        :param letter: letter given by the user
        """
        if to_append:
            if len(self.user_input) < 10:
                self.user_input += letter
        else:
            self.user_input = self.user_input[:-1]
        surface_input = self.font.render(self.user_input, True, Colors.DARK_GREEN.value)
        text_rect_input = surface_input.get_rect()
        text_rect_input.center = (self.screen_w / 2, self.screen_h * .5)
        self.screen.blit(surface_input, text_rect_input)
        pygame.display.update()

    def update(self, mouse):
        """
        Highlights buttons when the mouse is above them
        :param mouse: position of the mouse
        """
        self.button_ok.update_button(mouse)
