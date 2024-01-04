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
        
        self.weaponindex = weaponindex
        self.atk = WeaponSettings.weaponatk[weaponindex]
        self.owner = owner
        self.window = window
        
        self.attacking = False
        self.startattack = False
        self.dir = 1
        self.hasflip = False
        self.has_harmed = False
        self.cd = WeaponSettings.weaponas[weaponindex]
        self.key = None
        self.index = 0

        self.weapon_group.add(self)

    def update(self):

        self.dir = self.owner.dir
        self.rect.topleft = (self.owner.rect.x + self.dir*PlayerSettings.playerWidth // 2, self.owner.rect.y + PlayerSettings.playerHeight // 3)
        
        if self.dir == -1:
            self.cur_image = pygame.transform.flip(self.image, True, False)
        else:
            self.cur_image = self.image     #控制武器朝向

        if self.owner.startattack:
            self.startattack = True
            
        if self.startattack and not self.attacking:
            self.cd -= 1
            if self.cd < 0:
                self.attacking = True
                self.cd += WeaponSettings.weaponas[self.weaponindex] + 1 

        if self.attacking and self.index < 1:
            self.rect.x += self.dir * 10
            if not self.has_harmed:
                if len(pygame.sprite.spritecollide(self, self.monster_group, False))>0 and self.owner.tag != 'monster':
                    for monster in pygame.sprite.spritecollide(self, self.monster_group):
                        monster.hp -= self.atk
                    
                if pygame.sprite.spritecollide(self, self.player, False) and self.owner.tag != 'player':
                    self.player[0].hp -= self.atk
                self.has_harmed = True 
            self.index += 1
            
        elif self.index == 1:
            self.attacking = False
            self.startattack = False
            self.has_harmed = False
            self.index = 0

          
            
            

    def draw(self):
        self.window.blit(self.cur_image, self.rect)