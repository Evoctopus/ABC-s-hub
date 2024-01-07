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
        self.defence = NPCSettings.npcDefence[name] * difficulty
        self.atk = NPCSettings.npcAttack[name] * difficulty
        self.speed = NPCSettings.npcSpeed[name] * difficulty  

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
    

class Monster(NPC):
    def __init__(self, x, y, name, window, difficulty, player, paths):
        super().__init__(x, y, name, window, difficulty, player, paths)
        
        self.startattack = False
        self.beingattacked = False
        self.check = False
        self.skill = None
        self.tag = 'monster'

    def attack(self):
        pass    

    def image_update(self):

        if not self.startattack or Debuff.DIZZY in self.debuff:
            self.image = self.images[0]
        elif self.state == State.ATTACKING:
            self.image = self.attackimage()
        else:
            self.index = (self.index + 0.3) % self.len 
            self.image = self.images[math.floor(self.index)]
       
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image
        
    def attackimage(self):
        return None

    def state_update(self):
        
        if self.hp <= 0:
            self.state = State.DEAD
        else:
            self.attacking = self.weapon.attacking
            if self.check and not self.player.weapon.startattack and not self.player.weapon.cooling:
                self.check = False
                self.beingattacked = False

            if self.beingattacked and not self.check:
                self.check = True
                self.hp -= self.player.weapon.ATK - self.defence
                if self.player.weapon.skill == 'stab':
                    self.debuff.append(Debuff.REPELL)
                elif self.player.weapon.skill == 'spin':
                    self.debuff.append(Debuff.DIZZY)


    def pos_update(self):

        self.dis = math.hypot(self.player.rect.centerx - self.rect.centerx, self.player.rect.centery - self.rect.centery)
        if (self.dis <= MonsterSettings.DetectingRange[self.name]) and not Debuff.DIZZY in self.debuff:
            self.startattack = True
        if self.startattack:
            if self.dis == 0:
                self.dx, self.dy = 0, 0
            else:
                self.dx, self.dy = ((self.player.rect.centerx - self.rect.centerx) / self.dis * self.speed, 
                                    (self.player.rect.centery - self.rect.centery) / self.dis * self.speed)
            self.attack()    #跟踪玩家
        if not Debuff.DIZZY in self.debuff:
            if self.player.rect.centerx < self.rect.centerx: 
                self.dir = -1
            elif self.player.rect.centerx > self.rect.centerx:
                self.dir = 1


    def debuff_update(self):
         
        if Debuff.REPELL in self.debuff:
            self.dx = -self.dir * 20
            self.clicktock(3)
            if not self.isclocking:
                self.debuff.remove(Debuff.REPELL)
        elif Debuff.DIZZY in self.debuff:
            self.skill = None
            self.dx = 0
            self.dy = 0
            self.clicktock(30)
            if not self.isclocking:
                self.debuff.remove(Debuff.DIZZY)


    def draw(self):
        self.window.blit(self.image, self.rect)
        if self.state != State.DEAD:
            pygame.draw.rect(self.window, (255, 0, 0), [self.rect.x, self.rect.y - 10, self.hp*self.coord, 10], 0)
            if self.weapon != None:
                self.weapon.draw()    
            self.window.blit(self.namerender, (self.rect.x + self.size[0] // 2 - len(self.name) * 2 , self.rect.y - NPCSettings.Fontsize - 10))
            

class Knight(Monster):
    
    def __init__(self, x, y, name, window, difficulty, player, paths):
        super().__init__( x, y, name, window, difficulty, player, paths)
        self.weapon = Sword(self.window, self, f"./assets/weapon/Sword-cut/sword-1.png", 65, 55)
        self.attacking_method = AttackMethod.WEAPON

    def attack(self):
        
        if (self.dis <= MonsterSettings.AttackingRange[self.name] or self.weapon.cooling):
            self.state = State.ATTACKING
            self.dx = 0
            self.dy = 0
            
            if not self.weapon.cooling:
                self.skill = 'cut'
            else: self.skill = None
        else:
            self.state = State.ALIVE
            self.skill = None   
        
    def attackimage(self):
        return self.images[0]



