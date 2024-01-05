# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
import math


class Weapon(pygame.sprite.Sprite, Collidable):
    def __init__(self, window, owner):
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        self.window = window
        self.owner = owner
        self.image = None
        self.rect = None
        self.original = None
        self.images = None
        
        self.index = SwordSettings.cooldown
        
        self.atk = 0
        self.attacking = False
        self.dir = 1
        self.index = 0
        self.click = 0
        self.hasattack = False
        self.cooling = False
        self.isclocking = False

    def update(self):

        self.dir = self.owner.dir
        self.handpos = self.owner.rect.centerx - self.dir * self.width // 6, self.owner.rect.centery + 25
        if self.attacking:
            self.image = self.images[math.floor(self.index)] 
        else:
            self.image = self.original  #更新画面

        if self.dir == 1:
            self.rect.bottomleft = self.handpos
        else:
            self.rect.bottomright = self.handpos
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image   #控制位置和朝向
        
        if self.owner.startattack:
            self.attacking = True

        if self.attacking:
            self.attack(self.owner.skill)
        
        if self.cooling:
            self.reset()
        
    def attack(self):
        pass   

    def reset(self):
        pass

    def clicktock(self, time):
        if not self.isclocking:
            self.isclocking = True
            self.click = time
        else:
            self.click -= 1
            if self.click == 1:
                self.isclocking = False

    def rotate(self, angle):
        self.cur_image = pygame.transform.rotate(self.cur_image, angle)
        midbottom = self.rect.midbottom
        self.rect = self.cur_image.get_rect()
        self.rect.midbottom = [midbottom[0] - math.sin(angle * math.pi / 180)*self.height*1.5, midbottom[1]]

    def draw(self):
        self.window.blit(self.image, self.rect)
    

class Sword(Weapon):
    def __init__(self, window, owner):
        Weapon.__init__(self, window, owner)
        self.AS = SwordSettings.AS
        self.images = [pygame.transform.scale(pygame.image.load(f"./assets/weapon/Sword-cut/sword-1.png"), (65, 55))]
        self.index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.width = 65
        self.height = 55
        
    def attack(self, skill):
        self.len = SwordSettings.skillmsg[skill]
        self.images = [pygame.transform.scale(pygame.image.load(f"./assets/weapon/Sword-{skill}/sword-{i}.png"), (65, 55)) 
                       for i in range(1, self.len+1)]
        self.index += 1 / self.AS
        if self.index >= self.len - 1:
            self.index = 0
            self.attacking = False
            self.cooling = True
    
    def reset(self):
        self.clicktock(20)
        if not self.isclocking:
            self.cooling = False
    
    def update(self):

        self.dir = self.owner.dir
        self.handpos = self.owner.rect.centerx - self.dir * self.width // 6, self.owner.rect.centery + 25
        self.image = self.images[math.floor(self.index)]   #更新画面

        if self.dir == 1:
            self.rect.bottomleft = self.handpos
        else:
            self.rect.bottomright = self.handpos
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image   #控制位置和朝向
        
        if self.owner.startattack:
            self.attacking = True

        if self.attacking:
            self.attack(self.owner.skill)
        
        if self.cooling:
            self.reset()

    def clicktock(self, time):
        if not self.isclocking:
            self.isclocking = True
            self.click = time
        else:
            self.click -= 1
            if self.click == 1:
                self.isclocking = False
            
        
