# -*- coding:utf-8 -*-
import pygame

from Settings import *

from Special import *


class Collidable:
    def __init__(self, window, bgm):
      
        self.click = 0
        self.isclocking = False
        self.effect = pygame.sprite.Group()
        self.debuff = []
        self.window = window
        self.bgm = bgm

    def clicktock(self, time):
        if not self.isclocking:
            self.isclocking = True
            self.click = time
        else:
            self.click -= 1
            if self.click == 1:
                self.isclocking = False    #计时器
    

    