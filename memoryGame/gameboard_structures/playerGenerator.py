import pygame.font
from enums.colors import Colors
import pygame
from random import randint
from enums.difficulties import Difficulties


class PlayerGenerator:
    """
    Class that generates object for storing statistics of players as name, scored point and symbols that the player found
     Attributes
    ----------
    :arg location_x: x location of player stats
    :arg location_y: y location of player stats
    :arg size_w: width of stats
    :arg size_h: height of stats
    :arg name: nickname of player
    :arg points: points scored by player
    :arg symbols_scored: table of symbols that are scored by player
    :arg screen: screen where stats are displayed
    :arg: state_of_turn: firs or second turn of a player
    :arg symbols_seen: which symbols have been already seen
    :arg symbol_size: size of symbol
    :arg x_coord: x coordinate of symbol that is scored to be displayed in stats
    :arg y_coord: y coordinate of symbol that is scored to be displayed in stats
    :arg point_disp_coord: coordinates of points
    :arg point_disp_size: size of points
    :arg previous_symbol: previous symbol selected - for ai
    :arg text_rect_name: rectangle that is displayed around name of player whose turn is at the moment
    :arg surface_name: surface of players name
    :arg difficulty: difficulty of game - for AI level
    :arg num_of_boxes: number of elements in the game

    Parameters
    ----------
    :param screen: screen of the game
    :param location: location of stats on the screen
    :param size: size of stats
    :param name: name of player
    :param symbols: symbols that are in the game
    :param symbol_size: size of symbol to be displayed when player scores a point
    :param difficulty: difficulty of a game
    """
    def __init__(self, screen, location: tuple, size: tuple, name: str, symbols: dict, symbol_size: float, difficulty):
        self.location_x, self.location_y = location
        self.size_w, self.size_h = size
        self.name = name
        self.points = 0
        self.symbols_scored = []
        self.screen = screen
        self.state_of_turn = 0
        self.symbols_seen = symbols
        self.symbol_size = symbol_size
        self.x_coord = self.location_x + self.size_w / 2 - 2 * symbol_size
        self.y_coord = self.x_coord
        self.point_disp_xy = ()
        self.point_disp_size = ()
        self.previous_symbol = 0
        self.text_rect_name = None
        self.surface_name = None
        self.difficulty = difficulty
        self.num_of_boxes = 28

    def update_points(self):
        """
        Updates points scored by a player
        """
        self.points += 1
        pygame.draw.rect(self.screen, Colors.LIGHT_BLUE.value, [self.point_disp_xy[0], self.point_disp_xy[1],
                                                                self.size_w, self.point_disp_size[1]])
        font = pygame.font.SysFont('arial', int(0.08 * self.size_h))
        surface_points = font.render(f"PUNKTY: {self.points}", True, Colors.DARK_GREEN.value)
        text_rect_point = surface_points.get_rect()
        text_rect_point.x, text_rect_point.y = self.point_disp_xy
        text_rect_point.size = self.point_disp_size
        self.screen.blit(surface_points, text_rect_point)
        pygame.display.update()

    def set_name(self, name: str):
        """Sets player name"""
        self.name = name

    def get_points(self) -> int:
        """
        Gets player points
        :return: number of points
        """
        return self.points

    def update_turn(self, is_turn=False):
        """Updates turn by displaying red rectangle around player name"""
        if is_turn:
            pygame.draw.rect(self.screen, Colors.RED.value, [self.text_rect_name.x-2,
                                                             self.text_rect_name.y-2,
                                                             self.text_rect_name.width+4,
                                                             self.text_rect_name.height+4], 3)
        else:
            pygame.draw.rect(self.screen, Colors.LIGHT_BLUE.value, [self.text_rect_name.x-2,
                                                                    self.text_rect_name.y-2,
                                                                    self.text_rect_name.width+4,
                                                                    self.text_rect_name.height+4], 3)
        pygame.display.flip()

    def stats_initialize(self):
        """Initializes stats"""
        font = pygame.font.SysFont('arial', int(0.08 * self.size_h))

        self.surface_name = font.render(self.name, True, Colors.DARK_GREEN.value)
        surface_points = font.render(f"PUNKTY: {self.points}", True, Colors.DARK_GREEN.value)

        self.text_rect_name = self.surface_name.get_rect()

        text_rect_point = surface_points.get_rect()

        self.text_rect_name.x, self.text_rect_name.y = self.location_x + self.size_w / 2 - self.text_rect_name.width / 2, \
                                             self.location_y
        text_rect_point.x, text_rect_point.y = self.location_x + self.size_w / 2 - text_rect_point.width / 2, \
                                               self.text_rect_name.y + self.text_rect_name.height * 1.1

        # size and coords of points saved for updating
        self.point_disp_size = text_rect_point.size
        self.point_disp_xy = text_rect_point.x, text_rect_point.y

        self.y_coord = text_rect_point.y + self.text_rect_name.height

        self.screen.blit(self.surface_name, self.text_rect_name)
        self.screen.blit(surface_points, text_rect_point)
        pygame.display.update()

    def add_symbol(self, symbol: str, coordinates: int):
        """Adds symbol for symbols seen by player"""
        self.symbols_seen[symbol].append(coordinates)

    def score_symbol(self, symbol: str):
        """Adds symbol that is scored by a player to stats"""
        self.symbols_scored.append(symbol)

        imp = pygame.image.load(r'images/' + symbol + '.png')
        imp = pygame.transform.scale(imp, (self.symbol_size, self.symbol_size))
        self.screen.blit(imp, (self.x_coord, self.y_coord))
        pygame.display.flip()

        if self.points % 3 == 2:
            self.x_coord = self.location_x + self.size_w / 2 - 2 * self.symbol_size
            self.y_coord += self.symbol_size * 3 / 2
        else:
            self.x_coord += self.symbol_size * 3 / 2


class AIGenerator(PlayerGenerator):
    def change_difficulty(self, difficulty):
        """Changes the difficulty"""
        self.difficulty = difficulty

    def what_to_reveal(self, symbols_seen: dict, symbols_revealed: dict) -> int:
        """Decides what place should be revealed"""
        possible_choices = []
        not_choices = []
        choice = 0
        # iterate through symbols that were revealed and get n possible choices
        for symbol, was_revealed in symbols_revealed.items():
            if not was_revealed and len(symbols_seen[symbol]):
                possible_choices.append(symbols_seen[symbol])
            elif was_revealed:
                not_choices.append(symbols_seen[symbol])
        # check if there is symbol that has two revealed coordinates
        if self.difficulty == Difficulties.EASY:
            # EASY
            count_2 = 0
            for i in range(len(possible_choices)):
                if len(possible_choices[i]) == 2:
                    count_2 += 1

            for i in range(len(possible_choices)):
                if len(possible_choices[i]) == 2 and count_2 > 2:
                    choice = possible_choices[i][0] if self.state_of_turn == 0 else possible_choices[i][1]
                    if choice == self.previous_symbol:
                        choice = possible_choices[i][0]
                    break

            find_other_choice = True
            while find_other_choice:
                choice = randint(0, self.num_of_boxes-1)
                find_other_choice = False
                for i in not_choices:
                    if choice in i:
                        find_other_choice = True
                    if choice == self.previous_symbol:
                        find_other_choice = True

        elif self.difficulty == Difficulties.MEDIUM:
            # MEDIUM
            if len(possible_choices) > 3:
                possible_choices = possible_choices[:3]
            for i in range(len(possible_choices)):
                if len(possible_choices[i]) == 2:
                    choice = possible_choices[i][0] if self.state_of_turn == 0 else possible_choices[i][1]
                    if choice == self.previous_symbol:
                        choice = possible_choices[i][0]

                    break

            if choice == 0:
                find_other_choice = True
                while find_other_choice:
                    choice = randint(0, self.num_of_boxes-1)
                    find_other_choice = False
                    for i in not_choices:
                        if choice in i:
                            find_other_choice = True
                    if choice == self.previous_symbol:
                        find_other_choice = True
        else:
            # HARD
            for i in range(len(possible_choices)):
                if len(possible_choices[i]) == 2:
                    choice = possible_choices[i][0] if self.state_of_turn == 0 else possible_choices[i][1]
                    if choice == self.previous_symbol:

                        choice = possible_choices[i][0]

                    break

            # if nothing was found
            if choice == 0:
                # the hard level
                find_other_choice = True
                while find_other_choice:
                    choice = randint(0, self.num_of_boxes-1)
                    find_other_choice = False
                    for i in possible_choices + not_choices:
                        if choice in i:
                            find_other_choice = True

        if self.state_of_turn == 0:
            self.previous_symbol = choice
            self.state_of_turn = 1
        else:
            self.state_of_turn = 0
            self.previous_symbol = 0
        return choice
