# -*- coding:utf-8 -*-

from typing import Any
import pygame
import math
from random import randint


from Settings import *
from Attributes import *
from Weapon import *
from Coin import *


class NPC(pygame.sprite.Sprite, Collidable):
    def __init__(self, x, y, name, window, player, bgm, paths):
        # Initialize father classes
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self, window, bgm)

        self.images = [pygame.transform.scale(pygame.image.load(path), NPCSettings.npcSize[name])
                       for path in paths]
        self.size = NPCSettings.npcSize[name]
        self.player = player

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.index = 0
        self.state = State.ALIVE
        self.len = len(self.images)
        self.name = name
   
        self.namefont = pygame.font.Font(None, NPCSettings.Fontsize)
        self.namerender = self.namefont.render(self.name, True, NPCSettings.namecolor) #显示NPC的名字
        self.dir = 1

    def update(self):
        self.dx, self.dy = 0, 0
        self.state_update()
        if self.state == State.TALKING or self.state == State.STILL:
            self.image = self.images[0]
        else:
            self.pos_update()
            self.image_update()
            self.rect = self.rect.move(self.dx, self.dy) 

    def image_update(self):
        self.index = (self.index + 0.01) % self.len 
        self.image = self.images[math.floor(self.index)]
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image

    def pos_update(self):
        pass

    def state_update(self):
        pass

    def draw(self, dx=0, dy=0):
        self.draw_button()
        self.window.blit(self.namerender, (self.rect.centerx - self.namerender.get_width()/2 , 
                                           self.rect.y - NPCSettings.Fontsize))
        self.window.blit(self.image, self.rect)
    
    def draw_button(self):
        pass

class DialogNPC(NPC):
    def __init__(self, x, y, name, window, player, bgm, paths, patrollingRange=70):
        super().__init__(x, y, name, window, player, bgm, paths)
        self.type = NPCType.DIALOG
        self.button_index = 0
        self.button = [self.namefont.render('<  E  >', False, (255, 255, 255)), self.namefont.render('<    E    >', False, (255, 255, 255))]
        self.can_talk = False
        self.patrollingRange = patrollingRange
        self.before_rect = (x, y)
        self.speed = 3

    def pos_update(self):
        pass

    def draw_button(self):
         if self.can_talk:
            self.button_index = (self.button_index + 0.01) % 2 
            self.cur_button = self.button[math.floor(self.button_index)]
            self.window.blit(self.cur_button, 
                            (self.rect.centerx - self.cur_button.get_width() / 2, self.rect.centery - 80))
            
    def reset_talkCD(self):
        self.talkCD = NPCSettings.talkCD
        
class ShopNPC(NPC):
    def __init__(self, x, y, name, window, player, bgm, paths, patrollingRange=70):
        super().__init__(x, y, name, window, player, bgm, paths)
        self.type = NPCType.SHOP
        self.button_index = 0
        self.button = [self.namefont.render('<  E  >', False, (255, 255, 255)), self.namefont.render('<    E    >', False, (255, 255, 255))]
        self.can_talk = False
        self.patrollingRange = patrollingRange
        self.before_rect = (x, y)
    
    def draw_button(self):
        if self.can_talk:
            self.button_index = (self.button_index + 0.01) % 2 
            self.cur_button = self.button[math.floor(self.button_index)]
            self.window.blit(self.cur_button, 
                            (self.rect.centerx - self.cur_button.get_width() / 2, self.rect.centery - 80))


    





