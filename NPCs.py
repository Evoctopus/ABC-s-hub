# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
from Weapon import *
import math

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
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.index = 0
        self.len = len(paths)
        self.hp = NPCSettings.npcHP[name] * difficulty
        self.coord = 60 / self.hp
        self.window = window
        self.state = State.ALIVE
        self.type = None
        self.weapon = None

        self.name = name
        self.namefont = pygame.font.Font(None, NPCSettings.Fontsize)
        self.namerender = self.namefont.render(self.name, True, NPCSettings.namecolor) #显示NPC的名字

        self.initialPosition = x  # 记录初始位置
        self.speed = NPCSettings.npcSpeed[name]
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
            self.debuff()
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
    
    def debuff(self):
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
    

class Monster(NPC):
    def __init__(self, x, y, name, path, window, hp, player, Attack = 3, Defence = 1, Money = 15):
        super().__init__(x, y, name, path, window, hp, player)
        self.atk = Attack
        self.defence = Defence
        self.money = Money
        self.weapon = Sword(self.window, self, f"./assets/weapon/Sword-cut/sword-1.png", 65, 55)
        self.startattack = False
        self.beingattacked = False
        self.check = False
        self.skill = None
        self.tag = 'monster'

    def attack(self):
        self.dx, self.dy =  (self.player.rect.centerx - self.rect.centerx) / self.dis * self.speed, (self.player.rect.centery - self.rect.centery) / self.dis * self.speed
        if (self.dis <= 70 or self.weapon.cooling):
            self.dx = 0
            self.dy = 0
            if not self.weapon.cooling:
                self.skill = 'cut'
            else: self.skill = None
        else:
            self.skill = None     

    def image_update(self):
        if not self.startattack or self.state == State.DIZZY:
            self.image = self.images[0]
        else:
            self.index = (self.index + 0.3) % self.len 
            self.image = self.images[math.floor(self.index)]
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image

    def state_update(self):
        if self.hp <= 0:
            self.state = State.DEAD
        else:
            if self.check and not self.player.weapon.startattack and not self.player.weapon.cooling:
                self.check = False
                self.beingattacked = False

            if self.beingattacked and not self.check:
                self.check = True
                self.hp -= self.player.weapon.ATK - self.defence
                if self.player.weapon.skill == 'stab':
                    self.state = State.REPELL
                elif self.player.weapon.skill == 'spin':
                    self.state = State.DIZZY
                else:
                    self.state = State.ALIVE

    def pos_update(self):

        self.dis = math.hypot(self.player.rect.centerx - self.rect.centerx, self.player.rect.centery - self.rect.centery)
        if (self.dis <= MonsterSettings.DetectingRange) and self.state != State.DIZZY:
            self.startattack = True
        if self.startattack:
            self.attack()    #跟踪玩家
        if self.player.rect.centerx < self.rect.centerx: 
            self.dir = -1
        elif self.player.rect.centerx > self.rect.centerx:
            self.dir = 1


    def debuff(self):
         
        if self.state == State.REPELL:
            self.dx = -self.dir * 20
            self.clicktock(3)
            if not self.isclocking:
                self.state = State.ALIVE
        elif self.state == State.DIZZY:
            self.skill = None
            self.dx = 0
            self.dy = 0
            self.clicktock(30)
            if not self.isclocking:
                self.state = State.ALIVE


    def draw(self):
        self.window.blit(self.image, self.rect)
        pygame.draw.rect(self.window, (255, 0, 0), [self.rect.x, self.rect.y - 10, self.hp*self.coord, 10], 0)
        if self.state != State.DEAD:
            self.weapon.draw()    
            self.window.blit(self.namerender, (self.rect.x + self.size[0] // 2 - len(self.name) * 2 , self.rect.y - NPCSettings.Fontsize - 10))

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



