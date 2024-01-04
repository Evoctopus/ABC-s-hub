# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
from Weapon import *
import math

class NPC(pygame.sprite.Sprite, Collidable):
    def __init__(self, x, y, name, path, window):
        # Initialize father classes
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)

        self.image = pygame.image.load(path)
        self.image_right = pygame.transform.scale(self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.window = window
        self.npc_group.add(self)
        self.tag = 'npc'

        self.name = name
        self.namefont = pygame.font.Font(None, NPCSettings.Fontsize)
        self.namerender = self.namefont.render(self.name, True, NPCSettings.namecolor) #显示NPC的名字

        self.initialPosition = x  # 记录初始位置
        self.speed = NPCSettings.npcSpeed
        self.dir = 1
        self.patrollingRange = 70  # 巡逻范围
       
        self.talking = False
        self.talkCD = 0

    def update(self):
        if not self.talking:
            self.rect.x += self.speed * self.dir
            if abs(self.rect.x - self.initialPosition) > self.patrollingRange:
                self.dir *= -1  # 反转方向
                self.image = pygame.transform.flip(self.image, True, False)
            if self.talkCD > 0:
                self.talkCD -= 1
            
    def reset_talkCD(self):
        self.talkCD = NPCSettings.talkCD

    def draw(self, dx=0, dy=0):
        self.window.blit(self.namerender, (self.rect.x + NPCSettings.npcWidth // 2 - len(self.name) * 2 , self.rect.y - NPCSettings.Fontsize))
        self.window.blit(self.image, self.rect)


class DialogNPC(NPC):
    def __init__(self, x, y, name, dialog):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    
    def update(self, ticks):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

class ShopNPC(NPC):
    def __init__(self, x, y, name, items, dialog):
        super().__init__(x, y, name)

        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    
    def update(self, ticks):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    

class Monster(NPC):
    def __init__(self, x, y, name, path, window, weaponindex, HP = 50, Attack = 3, Defence = 1, Money = 15):
        super().__init__(x, y, name, path, window)
        self.atk = Attack
        self.tag = 'monster'
        self.defence = Defence
        self.money = Money
        self.hp = HP
        self.blood_k = 60 / HP
        self.speed = 3
        self.dx = 0 
        self.dy = 0
        self.weapon = Weapon(self.window, weaponindex, self)
        self.monster_group.add(self)
        self.startattack = False
        

    def attack(self, player):
        self.dx, self.dy =  (player.rect.centerx - self.rect.centerx) / self.dis * self.speed, (player.rect.centery - self.rect.centery) / self.dis * self.speed
        if (self.dis <= 90):
            self.dx = 0
            self.dy = 0
            self.startattack = True
        else:
            self.startattack = False

            
    def update(self, player):

        self.dis = math.hypot(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)

        if (self.dis <= MonsterSettings.DetectingRange):
            self.attack(player)
        if player.rect.centerx < self.rect.centerx: 
            self.dir = -1
            self.image = self.image_left
        elif self.dx > 0:
            self.dir = 1
            self.image = self.image_right
        self.weapon.update()
        self.rect = self.rect.move(self.dx, self.dy)

    def draw(self, dx=0, dy=0):
        self.window.blit(self.namerender, (self.rect.x + NPCSettings.npcWidth // 2 - len(self.name) * 2 , self.rect.y - NPCSettings.Fontsize - 10))
        self.window.blit(self.image, self.rect)
        pygame.draw.rect(self.window, [255, 0, 0], [self.rect.x, self.rect.y - 10, self.hp*self.blood_k, 10], 0)
        self.weapon.draw()    

    #def draw(self, window, dx=0, dy=0):
        #window.blit(self.image, self.rect)

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####



