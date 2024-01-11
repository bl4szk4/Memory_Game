from memoryGame.game import MemoryGame
import pygame

if __name__ == '__main__':
    pygame.init()
    memory_game = MemoryGame()
    while True:
        memory_game.game()
