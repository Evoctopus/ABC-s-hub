# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
from Weapon import *

class Player(pygame.sprite.Sprite, Collidable):
    def __init__(self, window):
        # Must initialize everything one by one here
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load(img), 
                            (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for img in GamePath.player]
        self.window = window
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.weapon = None
        self.hp = 100
        self.hp_coord = 60 / self.hp
        self.speed = 5
        self.tag = 'player'
        
        self.vert = 10
        self.acceleration = -2   #跳跃的相关变量

        self.dir = 1
        self.is_talking = False
        self.is_jumping = False
        self.skill = None
        
        self.weapon = Sword(self.window, self, f"./assets/weapon/Sword-cut/sword-1.png", 65, 55)

    def attr_update(self, addCoins = 0, addHP = 0, addAttack = 0, addDefence = 0):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def reset_pos(self, x=WindowSettings.width // 2, y=WindowSettings.height // 2):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def try_move(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update(self, key, events):

        
        if key[pygame.K_d] or key[pygame.K_w] or key[pygame.K_a] or key[pygame.K_s]:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
        else:
            self.image = self.images[0]

        if self.is_talking:
            # 如果不移动，显示静态图像
            self.index = 0
            self.image = self.images[self.index]
        else:
            dx = 0
            dy = 0
            if self.is_jumping:
                self.image = self.images[0]
                dy -= self.vert
                self.vert += self.acceleration
                if self.vert < -10:
                    self.vert = 10
                    self.is_jumping = False 
            
            if not self.weapon.startattack:
                if key[pygame.K_j]:
                    self.skill = 'cut'
                elif key[pygame.K_k]:
                    self.skill = 'stab'
                elif key[pygame.K_l]:
                    self.skill = 'longcut'
                elif key[pygame.K_i]:
                    self.skill = 'spin'
                elif key[pygame.K_o]:
                    self.skill = 'disappear'
                else:
                    self.skill = None
            else:
                self.skill = None

            if key[pygame.K_w] and self.rect.top > 0 :
                dy -= self.speed
            if key[pygame.K_s] and self.rect.bottom < WindowSettings.height:
                dy += self.speed
            if key[pygame.K_a] and self.rect.left > 0:
                dx -= self.speed
                self.dir = -1
            if key[pygame.K_d] and self.rect.right < WindowSettings.width:
                dx += self.speed
                self.dir = 1
            if key[pygame.K_SPACE]:
                self.is_jumping = True

            self.rect = self.rect.move(dx, dy)
              
        self.weapon.update() 
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)

            ##if pygame.sprite.spritecollide(self, scene.obstacles, False):
                # 遇到障碍物，取消移动
               # self.rect = self.rect.move(-dx, -dy)

            # 更新角色动画
            
    def draw(self):
        self.window.blit(self.image, self.rect)
        pygame.draw.rect(self.window, (255, 0, 0), [self.rect.x, self.rect.y - 10, self.hp*self.hp_coord, 10], 0)
        self.weapon.draw()
