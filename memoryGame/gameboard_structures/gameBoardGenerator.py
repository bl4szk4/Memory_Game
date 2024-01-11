import pygame

from memoryGame.camera_structures.cameraProcess import CameraProcess
from memoryGame.epson_structures.epsonConnector import Epson
from memoryGame.gameboard_structures.buttonGenerator import ButtonGenerator
from time import sleep
from utils.mouseDetection import mouse_detection
from memoryGame.gameboard_structures.symbolsGenerator import SymbolsGenerator
from enums.colors import Colors
from enums.difficulties import Difficulties
from memoryGame.gameboard_structures.playerGenerator import PlayerGenerator, AIGenerator
from memoryGame.windows.Windows import Windows
from random import shuffle
from enums.epsonInstructions import Instructions


class GameBoard(Windows):
    """Class that stores information about memoryGame board and prints it out to the screen

    Attributes
    ----------
    :arg _colors: colors of particular elements of the game board
    :arg coordinates: gets the dictionary where keys are symbols names and then to values will be added coordinates of
    those symbols on game board by methode shuffle_board
    :arg _size: stores sizes of particular elements
    :arg game_board_x/y: stores the top left coordinates of game board
    :arg elements_coordinates: stores the coordinates of blank places on the game board where symbols are revealed
    :arg coordinates_revealed: stores the position (as index of elements_coordinates table) of symbols that were revealed
    :arg num_of_symbols_revealed: stores coordinates of symbols that were revealed as indexes of the game board -> for AI
    :arg positions_of_symbols_unrevealed: stores the coordinates of symbols that are shown under the game board
    :arg is_symbol_revealed: stores in a dictionary as keys symbols names and as values bool whether the symbol is
    revealed or not
    :arg player_gamer: instance of a class Player for a real player
    :arg player_ai: instance of a class Player for a robot
    :arg num_of_boxes: how many boxes are on the board
    :arg robot: Epson robot class to send data and receive information
    :arg selected_coordinate: coordinate selected to be sent to a robot, also to check if player did not select the same
    coordinate twice in a row
    :arg turn_finished: used to synchronise info with main process
    :arg camera: camera class instance

    Parameters
    ----------
    :param robot: epson connector class instance
    :param camera: camera class instance
    :param screen: screen used to show the game on by pygame
    :param screen_w: the width of the game
    :param screen_h: the height of the game
    :param player: the name of the player
    """

    def __init__(self, robot: Epson, camera: CameraProcess, screen, screen_w, screen_h, player: str, difficulty=Difficulties.EASY):
        super().__init__(screen, screen_w, screen_h)
        self.background_colors = Colors.LIGHT_BLUE.value
        self.game_board_back_colors = Colors.BLACK.value
        self.game_board_front_colors = Colors.WHITE.value
        self.coordinates = SymbolsGenerator.generate_symbols_dict()
        self.player = player
        self.game_board_size = .5 * self.screen_h
        self.symbol_size = .6 * self.game_board_size / 6.0
        self.game_board_x = self.screen_w / 2 - self.game_board_size / 2
        self.game_board_y = .1 * self.screen_h
        self.elements_coordinates = []
        self.coordinates_revealed = []
        self.num_of_symbols_revealed = SymbolsGenerator.generate_symbols_dict()
        self.positions_of_symbols_unrevealed = SymbolsGenerator.generate_symbols_dict()
        self.is_symbol_revealed = SymbolsGenerator.generate_symbols_revealed()
        self.player_gamer = PlayerGenerator(self.screen, (0, .1 * self.screen_h), (.2 * self.screen_w,
                                                                                   self.game_board_size), player, self.coordinates, self.symbol_size, difficulty)
        self.player_ai = AIGenerator(self.screen, (self.game_board_x + self.game_board_size, .1 * self.screen_h),
                                         (.2 * self.screen_w, self.game_board_size), "AI", self.coordinates,
                                     self.symbol_size, difficulty)
        self.previous_symbol = ''
        self.num_of_boxes = 28
        self.robot = robot
        self.selected_coordinate = -1
        self.player_turn = True
        self.turn_finished = True
        self.camera = camera
        self.confirm_buttons = []

    def set_name(self, name: str):
        """Sets the name of the main player to the one given in the start"""
        self.player = name

    def check_game_over(self) -> bool:
        """Checks if there are symbols unrevealed to end the game"""
        max_points = max(self.player_gamer.get_points(), self.player_ai.get_points())
        if max_points > self.num_of_boxes / 2:
            return True
        else:
            return False

    def check_winner(self) -> int:
        """Returns 1 if the player won, 2 if Ai, 3 if there is a draw"""
        if self.player_gamer.get_points() > self.player_ai.get_points():
            return 1
        elif self.player_gamer.get_points() < self.player_ai.get_points():
            return 2
        else:
            return 3

    def show_winner(self, is_draw: bool, name: str = None):
        """Shows who won the game on screen"""
        if is_draw:
            winner = ButtonGenerator(self.screen, (self.screen_w / 2, self.game_board_y + 1.3 * self.game_board_size),
                                     Colors.RED.value, Colors.GRAY.value,
                                     'THERE IS A DRAW', 'consolas', int(0.05 * self.screen_h))
        else:
            winner = ButtonGenerator(self.screen, (self.screen_w / 2, self.game_board_y + 1.3 * self.game_board_size),
                            Colors.RED.value, Colors.GRAY.value,
                            'THE WINNER IS ' + name, 'consolas', int(0.05 * self.screen_h))
        winner.draw_button()

    def draw_game_board(self):
        """Draws the main memoryGame board on screen
            and creates a list containing white elements coordinates"""

        self.screen.fill(self.background_colors)

        # draw the main square
        pygame.draw.rect(self.screen, self.game_board_back_colors,
                         [self.game_board_x, self.game_board_y,
                          self.game_board_size, self.game_board_size])
        # draw the cubes holes
        cube_x = .1 * self.game_board_size + self.game_board_x
        cube_y = .1 * self.game_board_size + self.game_board_y
        # coordinates to be passed
        pass_coordinates = [[0, 4], [0, 5], [5, 4], [5, 5], [1, 5], [2, 5], [3, 5], [4, 5]]
        for i in range(6):
            for j in range(6):
                if [i, j] in pass_coordinates:
                    continue
                self.elements_coordinates.append([cube_x + i * (7/50) * self.game_board_size,
                                                  cube_y + j * (7/50) * self.game_board_size])
        self.confirm_buttons = [[cube_x + 0 * (7/50) * self.game_board_size,
                                 cube_y + 5 * (7/50) * self.game_board_size],
                                [cube_x + 2.5 * (7 / 50) * self.game_board_size,
                                 cube_y + 5 * (7 / 50) * self.game_board_size],
                                [cube_x + 5 * (7 / 50) * self.game_board_size,
                                 cube_y + 5 * (7 / 50) * self.game_board_size]
                                ]
        element = 0
        for i in range(6):
            for j in range(6):
                if [i, j] in pass_coordinates:
                    continue
                pygame.draw.rect(self.screen, self.game_board_front_colors,
                                 [self.elements_coordinates[element][0],
                                  self.elements_coordinates[element][1],
                                  self.symbol_size, self.symbol_size])
                element += 1
        self.show_elements()
        pygame.display.flip()
        self.player_gamer.set_name(self.player)
        self.player_gamer.stats_initialize()
        self.player_ai.stats_initialize()

    def element_focus_update(self, mouse_xy):
        """This method shows focus on game board elements by changing their color when mouse is focused on them"""
        for i in range(self.num_of_boxes):
            if mouse_detection((self.elements_coordinates[i][0], self.elements_coordinates[i][1]),
                               (self.symbol_size, None), mouse_xy) and i not in self.coordinates_revealed:
                pygame.draw.rect(self.screen, Colors.GRAY.value,
                                 [self.elements_coordinates[i][0],
                                  self.elements_coordinates[i][1],
                                  self.symbol_size, self.symbol_size])

            else:
                if i not in self.coordinates_revealed:
                    pygame.draw.rect(self.screen, self.game_board_front_colors,
                                     [self.elements_coordinates[i][0],
                                      self.elements_coordinates[i][1],
                                      self.symbol_size, self.symbol_size])

        pygame.display.flip()

    def shuffle_board(self):
        """Randomly selects a place for symbols on board - for non robot case"""
        coordinates = [x for x in range(self.num_of_boxes)]
        print(self.coordinates)
        shuffle(coordinates)
        for key in self.coordinates.keys():
            self.coordinates[key].append(coordinates.pop())
            self.coordinates[key].append(coordinates.pop())

    def show_elements(self):
        """Shows elements that are still not found under the game board
        first_coordinate calculates position of the first element to be shown
        symbol to be shown is stored in imp
        """
        img_col = 0
        img_row = 0
        first_coordinate = self.screen_w / 2 - 2 * (7/50) * self.game_board_size - self.symbol_size / 2
        for key in self.coordinates.keys():
            imp = pygame.image.load(r'images/' + key + '.png')
            imp = pygame.transform.scale(imp, (self.symbol_size, self.symbol_size))

            self.screen.blit(imp, (first_coordinate + img_col * self.game_board_size * 7 / 50,
                                   self.game_board_y + 1.1 * self.game_board_size + 7 / 50 * self.game_board_size * img_row))
            self.positions_of_symbols_unrevealed[key] = [first_coordinate + img_col * self.game_board_size * 7 / 50,
                                                         self.game_board_y + 1.1 * self.game_board_size + 7 / 50 * self.game_board_size * img_row]
            if img_col % 5 != 4:
                img_col += 1

            else:
                img_col = 0
                img_row += 1

    def get_coordinate(self, is_player_turn, mouse=None) -> bool:
        """Checks if the symbol can be revealed, if it has not been revealed yet, it adds the index of symbol
        to dicts and updates scores
        It also sends commands to epson scara robot
        """
        self.turn_finished = False

        self.player_turn = is_player_turn
        # to make sure that player has clicked on the right element
        player_selected_symbol = None

        # ai choice
        if not is_player_turn:
            player_selected_symbol = self.player_ai.what_to_reveal(self.num_of_symbols_revealed, self.is_symbol_revealed)
        # player's turn
        else:

            # stage of checking the place where player clicked on
            for i in range(self.num_of_boxes):
                if mouse_detection((self.elements_coordinates[i][0], self.elements_coordinates[i][1]),
                                   (self.symbol_size, None), mouse):
                    player_selected_symbol = i

        # player did not click on the element or selected the same element twice
        if (player_selected_symbol is None or self.selected_coordinate == player_selected_symbol) and is_player_turn:
            self.turn_finished = True
            return False

        self.selected_coordinate = player_selected_symbol
        self.element_focus_update((0, 0))
        # displays orange rectangle in a place of AI choice
        pygame.time.delay(10)
        pygame.draw.rect(self.screen, Colors.ORANGE.value,
                         [self.elements_coordinates[self.selected_coordinate][0],
                          self.elements_coordinates[self.selected_coordinate][1],
                          self.symbol_size, self.symbol_size])
        pygame.time.delay(10)
        pygame.display.flip()
        return True

    def get_symbol(self) -> bool:
        """
        Communication with epson robot to go to the specific coordinates and if the first time symbol is revealed
        from that coordinate - goes to camera
        """

        is_element = False

        # check if the element is in the memory
        for key, val in self.coordinates.items():
            if self.selected_coordinate in val:
                is_element = True
        # if element is in the memory - robot just shows it
        if is_element:
            response = self.robot.write_coordinates(self.selected_coordinate)
            if not response:
                return False
            while not self.robot.get_response(instruction=Instructions.CAMERA_POINT):
                pygame.time.delay(10)
            self.robot.reset_all()
            return True
        # if element is not in the memory - robot goes to the camera
        else:
            response = self.robot.write_coordinates(self.selected_coordinate, go_camera=True)
            if not response:
                return False
            for i in range(3):
                while not self.robot.get_response(instruction=Instructions.CAMERA_POINT):
                    pygame.time.delay(10)
                self.camera.capture_image()
                self.robot.next_camera()
                pygame.time.delay(100)
            self.robot.reset_all()
            response = self.robot.place_back()

            if not response:
                return False

            symbol_name = self.camera.predict()
            self.coordinates[symbol_name].append(self.selected_coordinate)
            return True

    def reveal_symbol(self):
        """
        Shows symbol on board and checks if a point was scored
        """
        for key, val in self.coordinates.items():
            if self.selected_coordinate in val:
                symbol = key

        if self.selected_coordinate not in self.num_of_symbols_revealed[symbol]:
            self.num_of_symbols_revealed[symbol].append(self.selected_coordinate)

        # shows the image of selected symbol
        pygame.draw.rect(self.screen, Colors.WHITE.value,
                         [self.elements_coordinates[self.selected_coordinate][0],
                          self.elements_coordinates[self.selected_coordinate][1],
                          self.symbol_size, self.symbol_size])
        imp = pygame.image.load(r'images/' + symbol + '.png')
        imp = pygame.transform.scale(imp, (self.symbol_size, self.symbol_size))
        self.screen.blit(imp, (self.elements_coordinates[self.selected_coordinate][0],
                               self.elements_coordinates[self.selected_coordinate][1]))
        pygame.display.flip()

        # player or AI scored a point
        if self.previous_symbol == symbol and not self.is_symbol_revealed[symbol]:
            self.is_symbol_revealed[symbol] = True

            if self.player_turn:
                self.player_gamer.score_symbol(symbol)
                self.player_gamer.update_points()
            else:
                self.player_ai.score_symbol(symbol)
                self.player_ai.update_points()

            # clears the scored symbol from the unrevealed symbols
            pygame.draw.rect(self.screen, Colors.LIGHT_BLUE.value,
                             [self.positions_of_symbols_unrevealed[symbol][0],
                              self.positions_of_symbols_unrevealed[symbol][1],
                              self.symbol_size, self.symbol_size])

            self.coordinates_revealed.append(self.selected_coordinate)
            self.previous_symbol = ''

        # the first turn of a player
        elif self.previous_symbol == '':
            self.coordinates_revealed.append(self.selected_coordinate)
            self.previous_symbol = symbol
            if not self.player_turn:
                pygame.time.wait(500)

        # second turn and player/AI did not score a point
        else:
            self.coordinates_revealed.pop()
            self.previous_symbol = ''
            self.selected_coordinate = -1
            pygame.time.wait(2000)
        while not self.robot.get_response(instruction=Instructions.HOME_POSITION):
            pygame.time.delay(10)
        self.element_focus_update((0, 0))
        self.turn_finished = True
