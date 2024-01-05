# -*- coding:utf-8 -*-

import pygame
from GameManager import GameManager

def main():
    pygame.init()
    clock = pygame.time.Clock()
    manager = GameManager()

    while True:

        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        manager.update()
        manager.render()
        pygame.display.flip()

if __name__ == "__main__":
    main()