import pygame, sys
from modules import interface

def start_concentration():
    i = interface.Interface()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        i.start_game()
        pygame.display.update()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    start_concentration()
