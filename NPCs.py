# -*- coding:utf-8 -*-

import pygame
import math
from random import randint


from Settings import *
from Attributes import *
from Weapon import *
from Coin import *


class NPC(pygame.sprite.Sprite, Collidable):
    def __init__(self, x, y, name, window, difficulty, player, paths):
        # Initialize father classes
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load(path), NPCSettings.npcSize[name])
                       for path in paths]
        self.size = NPCSettings.npcSize[name]
        self.player = player
        self.dead = pygame.transform.scale(pygame.image.load(f"./assets/npc/{name}/dead.png"), NPCSettings.npcSize[name])
        self.dizzy = [pygame.transform.scale(pygame.image.load(f"./assets/specialeffect/dizzy/{index}.png"), 
                                             NPCSettings.npcSize[name]) for index in range(1, 4)]
        self.dizzy_index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.index = 0
        self.len = len(paths)

        self.hp = NPCSettings.npcHP[name] * difficulty
        self.defence = NPCSettings.npcDefence[name] * difficulty
        self.atk = NPCSettings.npcAttack[name] * difficulty
        self.speed = NPCSettings.npcSpeed[name] * difficulty  
        self.money = (0, 0)  #(gold, silver)

        self.coord = 60 / self.hp
        self.window = window
        self.state = State.ALIVE
        self.debuff = []
        self.type = None
        self.weapon = None
        self.attacking_method = None
        self.attacking = False
        self.hasattacked = False

        self.name = name
        self.namefont = pygame.font.Font(None, NPCSettings.Fontsize)
        self.namerender = self.namefont.render(self.name, True, NPCSettings.namecolor) #显示NPC的名字

        self.initialPosition = x  # 记录初始位置
        self.dir = 1
        self.dx = 0
        self.dy = 0
       
        self.patrollingRange = 70  # 巡逻范围
       
        self.talkCD = 0

    def update(self):
        self.state_update()
        if self.state == State.DEAD:
            self.dx = 0
            self.dy = 0
            self.image = self.dead
            if self.dir == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.image = self.image
           
        else:
            self.pos_update()
            self.image_update()
            self.debuff_update()
            if self.weapon != None:
                self.weapon.update()
            self.rect = self.rect.move(self.dx, self.dy) 

    def image_update(self):
        self.index = (self.index + 1) % self.len 
        self.image = self.images[math.floor(self.index)]
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image

    def pos_update(self):
        
        if abs(self.rect.x - self.initialPosition) > self.patrollingRange:
            self.dir *= -1  # 反转方向4
        self.dx = self.speed * self.dir

    def reset_talkCD(self):
        self.talkCD = NPCSettings.talkCD
    
    def debuff_update(self):
        pass

    def state_update(self):
        pass

    def draw(self, dx=0, dy=0):
        self.window.blit(self.namerender, (self.rect.x + self.size[0] // 2 - len(self.name) * 2 , self.rect.y - NPCSettings.Fontsize))
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
    





