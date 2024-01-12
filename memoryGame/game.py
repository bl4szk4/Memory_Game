import sys
import time

import pygame

from enums.colors import Colors
from enums.screens import Screens
from enums.difficulties import Difficulties
from memoryGame.camera_structures.cameraProcess import CameraProcess
from memoryGame.gameboard_structures.gameBoardGenerator import GameBoard
from memoryGame.windows.menuWindows import MenuWindows
from memoryGame.windows.inputWindow import InputWindow
from memoryGame.windows.settingsWindow import SettingsWindow
from memoryGame.epson_structures.epsonConnector import Epson
from threading import Thread


class MemoryGame:
    """
    Main class that manages whole game, including windows change, creating instances of classes, changing players' turns

    Attributes
    ----------
    :arg camera: instance of camera class
    :arg robot: instance of robot class
    :arg player_name: basic nick of a player
    :arg width: main window width
    :arg height: main window height
    :arg screen_pygame: main screen
    :arg menu_screen: menu window
    :arg input_screen: input window for nickname input
    :arg settings_screen: settings window for difficulty selection and camera calibration
    :arg mouse_pos: tuple for storing x and y coordinates of mouse
    :arg is_screen_initialized: boolean for storing information if window is initialized
    :arg screen: stores enum Screen of what screen is now being displayed
    :arg is_player_turn: boolean, True if a real player is now playing his turn
    :arg state_of_turn: stores information about what stage of turn is now being played
    :arg difficulty: enum Difficulty, predefined as medium
    :arg is_game_over: boolean, True if game is finished
    :arg board_screen: window for a game board
    """
    def __init__(self):
        self.camera = CameraProcess()
        self.camera.start_camera()
        self.robot = Epson()
        self.player_name = "Gracz"
        self.width = 1020
        self.height = 1020
        self.screen_pygame = pygame.display.set_mode((self.height, self.width))
        pygame.display.set_caption("MemoryGame")
        self.menu_screen = MenuWindows(self.screen_pygame, self.width, self.height)
        self.input_screen = InputWindow(self.screen_pygame, self.width, self.height)
        self.settings_screen = SettingsWindow(self.screen_pygame, self.width, self.height)
        self.mouse_pos = ()
        pygame.init()
        self.is_screen_initialized = False
        self.screen = None
        self.is_player_turn = True
        self.state_of_turn = 0
        self.difficulty = Difficulties.MEDIUM
        self.is_game_over = False
        self.board_screen = None

    def game(self):
        """
        Manages switching between screens and changing players turn
        """
        # Menu screen
        if self.screen is None:
            self.menu_screen.menu_init()
            self.screen = Screens.MENU

        self.mouse_pos = pygame.mouse.get_pos()

        if self.screen == Screens.MENU:
            if not self.is_screen_initialized:
                self.menu_screen.menu_init()
                if self.robot.c is None:
                    if not self.robot.start_connection():
                        font = pygame.font.SysFont('consolas', int(self.width / 20))
                        surface_info = font.render("SPRAWDŹ POŁĄCZENIE Z ROBOTEM", True, Colors.RED.value)
                        text_rect_info = surface_info.get_rect()
                        text_rect_info.center = (self.width / 2, self.height / 2)
                        self.screen_pygame.blit(surface_info, text_rect_info)
                        pygame.display.update()
                        pygame.time.delay(3000)
                        sys.exit()

                self.is_screen_initialized = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_screen.button_start.on_focus(self.mouse_pos):
                        self.screen = Screens.INPUT
                        self.is_screen_initialized = False
                    elif self.menu_screen.button_options.on_focus(self.mouse_pos):
                        self.screen = Screens.OPTIONS
                        self.is_screen_initialized = False
            self.menu_screen.update_buttons(self.mouse_pos)

        # Game screen
        elif self.screen == Screens.GAME:
            if not self.is_screen_initialized:
                self.board_screen = GameBoard(self.robot, self.camera, self.screen_pygame,
                                              self.height, self.width, self.player_name)
                self.board_screen.draw_game_board()
                self.is_screen_initialized = True
                self.board_screen.player_gamer.update_turn(True)
                self.board_screen.player_ai.change_difficulty(self.difficulty)

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_game()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # clicked
                        self.mouse_pos = pygame.mouse.get_pos()
                        # is player turn
                        if self.state_of_turn < 2 and not self.is_game_over:
                            if self.board_screen.turn_finished:
                                turn = Thread(name='turn', target=self.player_turn, daemon=True)
                                turn.start()
                            # clear all events that might be qued - like mouse clicks while AI turn
                            pygame.event.clear()
                if self.board_screen.turn_finished:
                    self.board_screen.element_focus_update(self.mouse_pos)

            # game over
            if self.is_game_over:
                who_won = self.board_screen.check_winner()
                if who_won == 1:
                    self.board_screen.show_winner(False, self.player_name)
                elif who_won == 2:
                    self.board_screen.show_winner(False, 'ROBOT')
                else:
                    self.board_screen.show_winner(True)
                pygame.time.delay(5000)
                self.board_screen = None
                self.screen = Screens.MENU
                self.is_screen_initialized = False

        # Input name screen
        elif self.screen == Screens.INPUT:
            if not self.is_screen_initialized:
                self.input_screen.input_init()
                self.is_screen_initialized = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_screen.button_ok.on_focus(self.mouse_pos):
                        if len(self.input_screen.user_input) != 0:
                            # if player typed his nickname
                            self.player_name = self.input_screen.user_input
                            self.board_screen.set_name(self.player_name)
                        self.screen = Screens.GAME
                        self.is_screen_initialized = False
                elif event.type == pygame.KEYDOWN:
                    # backspace clears previous letter
                    if event.key == pygame.K_BACKSPACE:
                        self.input_screen.input_init()
                        self.input_screen.text_update(False)
                    # enter works the same as OK button
                    elif event.key == pygame.K_RETURN:
                        if len(self.input_screen.user_input) != 0:
                            self.player_name = self.input_screen.user_input
                            self.board_screen.set_name(self.player_name)
                        self.screen = Screens.GAME
                        self.is_screen_initialized = False
                    # any other key as a letter
                    else:
                        self.input_screen.input_init()
                        self.input_screen.text_update(True, event.unicode)

            self.input_screen.update(self.mouse_pos)

        # settings window
        elif self.screen == Screens.OPTIONS:
            if not self.is_screen_initialized:
                self.settings_screen.settings_init()
                self.is_screen_initialized = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # difficulties
                    if self.settings_screen.button_easy.on_focus(mouse=self.mouse_pos):
                        self.difficulty = Difficulties.EASY
                        self.is_screen_initialized = False
                        self.screen = Screens.MENU
                    elif self.settings_screen.button_medium.on_focus(mouse=self.mouse_pos):
                        self.difficulty = Difficulties.MEDIUM
                        self.is_screen_initialized = False
                        self.screen = Screens.MENU
                    elif self.settings_screen.button_hard.on_focus(mouse=self.mouse_pos):
                        self.difficulty = Difficulties.HARD
                        self.is_screen_initialized = False
                        self.screen = Screens.MENU
                    # camera calibration
                    elif self.settings_screen.button_camera_position.on_focus(mouse=self.mouse_pos):
                        self.robot.test_camera(True)
                        self.camera.calibrate_camera()
                        self.robot.test_camera()
                        self.is_screen_initialized = False
                        self.screen = Screens.MENU
            self.settings_screen.update_buttons(mouse=self.mouse_pos)

    def ai_turn(self):
        """
         The turn of AI
        """
        self.state_of_turn = 0

        if not self.board_screen.check_game_over():
            # the ai turn twice
            pygame.time.delay(10)
            self.board_screen.element_focus_update((0, 0))
            self.board_screen.player_gamer.update_turn(False)
            self.board_screen.player_ai.update_turn(True)
            pygame.time.delay(10)
            for i in range(2):
                self.board_screen.get_coordinate(is_player_turn=False)
                self.board_screen.get_symbol()
                self.board_screen.reveal_symbol()
        if not self.board_screen.check_game_over():
            self.board_screen.player_gamer.update_turn(True)
            self.board_screen.player_ai.update_turn(False)
        else:
            self.is_game_over = True

    def player_turn(self):
        """The turn of a player"""
        # if previous turn has finished
        if self.board_screen.turn_finished:
            # if player clicked on element
            if self.board_screen.get_coordinate(mouse=self.mouse_pos, is_player_turn=True):
                # if coordinates are correct
                no_error = self.board_screen.get_symbol()
                if no_error:
                    self.board_screen.reveal_symbol()
                    self.state_of_turn += 1
                else:
                    self.board_screen.element_focus_update((0, 0))
                if self.state_of_turn == 2:
                    self.ai_turn()

    def quit_game(self):
        """Quits the game"""
        self.robot.close_connection()
        self.camera.stop_camera()
        sys.exit()
