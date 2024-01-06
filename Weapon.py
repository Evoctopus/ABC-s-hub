# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
import math


class Weapon(pygame.sprite.Sprite, Collidable):
    def __init__(self, window, owner, gamepath, width, height):
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        self.width = width
        self.height = height
        self.window = window
        self.owner = owner
        
        self.index = 0
        self.original = pygame.transform.scale(pygame.image.load(gamepath), (width, height))
        self.images = [pygame.transform.scale(pygame.image.load(gamepath), (width, height))]
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        self.atk = 0
        self.attacking = False
        self.startattack = False
        self.dir = 1

        self.attackingindex = None
        self.cooling = False
       

    def update(self):

        self.dir = self.owner.dir
        self.handpos = self.owner.rect.centerx - self.dir * self.width // 6, self.owner.rect.centery + 25
        if self.startattack:
            self.image = self.images[math.floor(self.index)] 
        else:
            self.image = self.original  #更新画面

        self.pos_update()
        
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image   #控制位置和朝向
        
        if self.owner.skill != None and not self.cooling:
            self.startattack = True

        if self.startattack:
            self.attack(self.owner.skill)
        
        if self.cooling:
            self.reset()

    def attack(self):
        pass   

    def reset(self):
        pass

    

    def rotate(self, angle):
        self.cur_image = pygame.transform.rotate(self.cur_image, angle)
        midbottom = self.rect.midbottom
        self.rect = self.cur_image.get_rect()
        self.rect.midbottom = [midbottom[0] - math.sin(angle * math.pi / 180)*self.height*1.5, midbottom[1]]
    
    def pos_update(self):
        pass

    def draw(self):
        self.window.blit(self.image, self.rect)
    

class Sword(Weapon):
    def __init__(self, window, owner, gamepath, width, height):
        Weapon.__init__(self, window, owner, gamepath, width, height)
        self.AS = None
        self.ATK = None
        self.skill = None
        
    def attack(self, skill):
        if skill != None:
            self.skill = skill
        self.msg = SwordSettings.skillmsg[self.skill]
        self.len = self.msg[0]
        self.AS = self.msg[2]
        self.ATK = self.msg[3]

        self.attackingindex = self.msg[4]
        self.images = [pygame.transform.scale(pygame.image.load(f"./assets/weapon/Sword-{self.skill}/sword-{i}.png"), self.msg[1]) 
                       for i in range(1, self.len+1)]
        self.index += 1 / self.AS[0]
        if self.index >= self.attackingindex:
            self.attacking = True
        if self.index >= self.len - 1:
            self.index = 0
            self.attacking = False
            self.startattack = False
            self.skill = None
            self.cooling = True
    
    
    def reset(self):
        self.clicktock(self.AS[1])
        if not self.isclocking:
            self.cooling = False
            

    def pos_update(self):
        if self.skill == 'cut':
            if self.dir == 1:
                self.rect.bottomleft = self.handpos
            elif self.dir == -1:
                self.rect.bottomright = self.handpos
        elif self.skill == 'stab':
            if self.dir == 1:
                self.rect.midleft = self.handpos
            else:
                self.rect.midright = self.handpos
        else:
            if self.dir == 1:
                self.rect.bottomleft = self.handpos
            elif self.dir == -1:
                self.rect.bottomright = self.handpos
    
    
            
        
