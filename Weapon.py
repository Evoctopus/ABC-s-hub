# -*- coding:utf-8 -*-

import pygame
import math

from Settings import *
from Attributes import *
from random import randint


class Weapon(pygame.sprite.Sprite, Collidable):
    def __init__(self, window, owner, gamepath, width, height, bgm):
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self, window, bgm)
        self.size = (width, height)
     
        self.owner = owner
        self.index = 0
        
        self.images = [pygame.transform.scale(pygame.image.load(paths), (width, height)) for paths in gamepath]
        self.original = self.images[0]
        self.image = self.images[0]
        self.len = len(self.images)
        self.rect = self.image.get_rect()

        self.atk = 0
        self.hasattacked = False
        self.attacking = False
        self.startattack = False
        self.dir = 1

        self.attackingindex = None
        self.cooling = False

    def image_update(self):  

        if self.startattack:
            self.image = self.images[math.floor(self.index)] 
        else:
            self.image = self.original

        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image

    def get_hanpos(self):
        self.handpos =  self.owner.rect.centerx - self.dir * self.size[0] // 6, self.owner.rect.centery + 25
    
    def update(self):

        self.atk *= self.owner.atk
        self.dir = self.owner.dir
        self.image_update()
        self.get_hanpos()
        self.pos_update()
        
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
    

class Claw(Weapon):
    def __init__(self, window, owner, gamepath, width, height, bgm):
        super().__init__(window, owner, gamepath, width, height, bgm)
        self.atk = 1
        self.attackingindex = 2

    def get_hanpos(self):
        self.handpos = self.owner.rect.centerx - self.dir * self.size[0] // 6, self.owner.rect.centery + 25

    def pos_update(self):
        if self.dir == 1:
            self.rect.bottomleft = self.handpos
        elif self.dir == -1:
            self.rect.bottomright = self.handpos
        
    def image_update(self): 
        if self.startattack:
            self.image = self.images[math.floor(self.index)] 
            self.index += 0.5
            if self.index >= self.len - 1:
                self.index = 0
                self.attacking = False
                self.startattack = False
                self.hasattacked = False
                self.skill = None
                self.cooling = True
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image
    
    def attack(self, skill):
        if skill != None:
            self.skill = skill
        if self.index >= self.attackingindex and not self.attacking:
            self.attacking = True
            self.bgm.addsound('hit')

class Sword(Weapon):
    def __init__(self, window, owner, gamepath, width, height, bgm):
        Weapon.__init__(self, window, owner, gamepath, width, height, bgm)
        self.AS = None
        self.skill = None
        self.playing = False
        self.buff = []
        self.swordplay = None
        self.playing_index = [1, 3, 4]
        self.handpos = self.get_hanpos()
        
    def attack(self, skill):
        if skill != None:
            self.skill = skill
        self.msg = SwordSettings.skillmsg[self.skill]
        self.len = self.msg[0]
        self.AS = self.msg[2]
        self.atk = self.msg[3] * self.owner.atk
        self.attackingindex = self.msg[4]
        self.images = [pygame.transform.scale(pygame.image.load(f"./assets/weapon/Sword-{self.skill}/sword-{i}.png"), self.msg[1]) 
                    for i in range(1, self.len+1)]
        if self.owner.tag == 'player':
            self.get_buff()
        self.index += 1 / self.AS[0]
        if self.index >= self.attackingindex:
            self.attacking = True
            if self.index == self.attackingindex:
                self.bgm.addsound('hit')
        if self.index >= self.len - 1:
            self.clear_attr()    

    def get_buff(self):
        if self.skill != 'disappear':
            if randint(1, 4) == 1:
                if self.skill == 'stab' and self.owner.buff_get['REPELL']:
                    self.buff = [Debuff.REPELL]
                elif self.skill == 'spin' and self.owner.buff_get['DIZZY']:
                    self.buff = [Debuff.DIZZY]
                elif self.skill == 'cut' and self.owner.buff_get['FROZEN']:
                    self.buff = [Debuff.FROZEN]
                elif self.skill == 'longcut' and self.owner.buff_get['BURNING']:
                    self.buff = [Debuff.BURNING]
            else:
                self.buff = []
        elif  self.swordplay == None:
                self.swordplay = SwordPlay(self, self.window, self.bgm, BuffSettings.swordplay)
                self.owner.sword_cd = 200

    def clear_attr(self):
        self.index = 0
        self.attacking = False
        self.startattack = False
        self.skill = None
        self.cooling = True
        self.buff = []

    def reset(self):
        self.clicktock(self.AS[1])
        if not self.isclocking:
            self.cooling = False
            self.hasattacked = False
            
    def pos_update(self):
        if self.skill == 'stab':
            if self.dir == 1:
                self.rect.midleft = self.handpos
            else:
                self.rect.midright = self.handpos
        else:
            if self.dir == 1:
                self.rect.bottomleft = self.handpos
            elif self.dir == -1:
                self.rect.bottomright = self.handpos
    
    def draw(self):
        self.window.blit(self.image, self.rect)
        if self.swordplay != None and not self.swordplay.isdisappear():
            self.swordplay.update()
            self.swordplay.draw()
        else:
            self.swordplay = None    
         
        
