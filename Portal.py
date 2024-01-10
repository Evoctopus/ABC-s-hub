# -*- coding:utf-8 -*-

from Settings import *

import pygame
import math

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, name, window, text, GOTO:SceneType, flip=False):
        super().__init__()
        self.window = window
        self.goto = GOTO
        self.image = pygame.transform.scale(pygame.image.load(f'./assets/background/{name}.png'), (PortalSettings.width, PortalSettings.height))
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.index = 0
        self.blink = False
        self.font = pygame.font.Font(None, PortalSettings.FontSize)
        self.text = self.font.render(text, False, (255, 255, 255))
        self.font = pygame.font.Font(None, PortalSettings.ButtonSize)
        self.button = [self.font.render('<  E  >', False, (255, 255, 255)), self.font.render('<    E    >', False, (255, 255, 255))]
        self.len = [self.button[0].get_width(), self.button[1].get_width(), self.text.get_width()]

    
    def draw(self):
        if self.blink:
            self.index = (self.index + 0.1) % 2 
            self.window.blit(self.text, (self.rect.centerx - self.len[2] / 2, self.rect.centery - 70))
            self.window.blit(self.button[math.floor(self.index)], 
                            (self.rect.centerx - self.len[math.floor(self.index)] / 2, self.rect.centery - 45))
        self.window.blit(self.image, self.rect)
