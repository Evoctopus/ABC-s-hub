# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *



class Weapon(pygame.sprite.Sprite, Collidable):
    def __init__(self, window, weaponindex, owner):
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(GamePath.weapon[weaponindex]), (WeaponSettings.weaponwidth, WeaponSettings.weaponheight)) 
        self.image = pygame.transform.flip(self.image, True, False)
        self.cur_image = self.image
        self.rect = self.image.get_rect()
        
        self.atk = WeaponSettings.weaponatk[weaponindex]
        self.owner = owner
        self.window = window
        
        self.attacking = False
        self.dir = 1
        self.hasflip = False
        self.index = 5
        self.key = None

    def update(self):

        self.rect.topleft = (self.owner.rect.x + self.dir*PlayerSettings.playerWidth // 2, self.owner.rect.y + PlayerSettings.playerHeight // 3)
        self.dir = self.owner.dir
        if self.dir == -1:
            self.cur_image = pygame.transform.flip(self.image, True, False)
        else:
            self.cur_image = self.image
            
        if self.attacking:
            self.rect.x += self.dir * 10
            self.attacking = False
            
            

    def draw(self):
        self.window.blit(self.cur_image, self.rect)