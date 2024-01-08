import pygame
import math
from random import randint

from NPCs import *
from Settings import *
from Attributes import *
from Weapon import *



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
            if Debuff.DIZZY in self.debuff:
                self.window.blit(self.dizzy[math.floor(self.dizzy_index)], (self.rect[0], self.rect[1] - self.size[1]/2))
                self.dizzy_index = (self.dizzy_index + 0.4) % 2
            pygame.draw.rect(self.window, (255, 0, 0), [self.rect.x, self.rect.y - 10, self.hp*self.coord, 10], 0)
            if self.weapon != None:
                self.weapon.draw()    
            self.window.blit(self.namerender, (self.rect.x + self.size[0] // 2 - len(self.name) * 2 , self.rect.y - NPCSettings.Fontsize - 10))
            

class Knight(Monster):
    
    def __init__(self, x, y, name, window, difficulty, player, paths):
        super().__init__( x, y, name, window, difficulty, player, paths)
        self.weapon = Sword(self.window, self, f"./assets/weapon/Sword-cut/sword-1.png", 65, 55)
        self.attacking_method = AttackMethod.WEAPON
        self.money = (2, 1)

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