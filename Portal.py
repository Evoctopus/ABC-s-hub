# -*- coding:utf-8 -*-

from Settings import *

import pygame
import math

from Settings import SceneType

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, name, window, text, GOTO:SceneType=None, flip=False):
        super().__init__()
        self.window = window
        self.goto = GOTO
        self.image = pygame.transform.scale(pygame.image.load(f'./assets/background/{name}.png'), PortalSettings.PortalSize)
        self.size = PortalSettings.PortalSize
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.before_rect = x, y
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

class EndPortal(Portal):
    def __init__(self, x, y, name, window, text, GOTO: SceneType = None, flip=False):
        super().__init__(x, y, name, window, text, GOTO, flip)
        self.images = [pygame.transform.scale(pygame.image.load(f'./assets/background/endportal/appear/{index}.png'),
                                              PortalSettings.EndPortalSize) for index in range(1, 27)]
        self.image_len = len(self.images)
        self.image_index = -0.5
        self.image = self.images[0]
        self.state = State.APPEAR
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def draw(self):
        #pygame.draw.rect(self.window, Color.Yellow, [self.rect.topleft[0], self.rect.topleft[1], 200, 200], 1)
        if self.blink:
            self.index = (self.index + 0.1) % 2 
            self.window.blit(self.text, (self.rect.centerx - self.len[2] / 2 + 15, self.rect.centery - 120))
            self.window.blit(self.button[math.floor(self.index)], 
                            (self.rect.centerx - self.len[math.floor(self.index)] / 2 + 15, self.rect.centery - 95))
            
        self.image_index = (self.image_index + 0.5) % self.image_len
        if self.image_index >= self.image_len - 1 and self.state == State.APPEAR:
            self.images = [pygame.transform.scale(pygame.image.load(f'./assets/background/endportal/{index}.png'),
                            PortalSettings.EndPortalSize) for index in range(1, 16)]
            self.image_index = 0
            self.image_len = len(self.images)
            self.state = State.STILL
        self.image = self.images[math.floor(self.image_index)]
        self.window.blit(self.image, self.rect)


class Buddha(Portal):
    def __init__(self, x, y, name, window, text):
        super().__init__(x, y, name, window, text)
        self.image = pygame.transform.scale(self.image, PortalSettings.BuddhaSize)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.size = PortalSettings.BuddhaSize

    
    def draw(self):
        if self.blink:
            self.index = (self.index + 0.1) % 2 
            self.window.blit(self.button[math.floor(self.index)], 
                            (self.rect.centerx - self.len[math.floor(self.index)] / 2, self.rect.centery - 85))
            
        self.window.blit(self.text, (self.rect.centerx - self.len[2] / 2, self.rect.centery - 110))
        self.window.blit(self.image, self.rect)