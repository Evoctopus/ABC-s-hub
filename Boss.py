import pygame

from Settings import *
from Attributes import *
from Weapon import *
import math



class Demon(pygame.sprite.Sprite, Collidable):
    def __init__(self, x, y, window, player, bgm) :
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load(f"./assets/npc/demon/idle/{i}.png"), NPCSettings.npcSize['demon']) 
                       for i in range(1, 15)]
        self.bgm = bgm
        self.width, self.height = NPCSettings.npcSize['demon']
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.attack_pos = self.rect.bottomleft
        self.player = player
        self.window = window
        self.action = 'idle'
        self.name = 'LUCIFER NIGHTFALL'
        self.hp = 500
        self.speed = 20
        self.atk = 20
        self.defence = 50
        self.debuff = []
        self.state = State.ALIVE
        self.attacking_method = AttackMethod.FIST
        self.check = False
        self.beingattacked = False
        self.index = 0
        self.dir = 1
        self.completelydead = False

        self.namefont = pygame.font.Font(None, NPCSettings.Fontsize)
        self.namerender = self.namefont.render(self.name, True, NPCSettings.namecolor)

    def update(self):
        self.msg = DemonSettings.demonmsg[self.action]
        self.len = self.msg[0]
        # self.AS = self.msg[2]
        # self.ATK = self.msg[3]
        # self.attackingindex = self.msg[4]
        self.images = [pygame.transform.scale(pygame.image.load(f"./assets/npc/demon/{self.action}/{i}.png"), NPCSettings.npcSize['demon']) 
                       for i in range(1, self.len)]
        self.state_update()
        self.image_update()
        if self.state == State.DEAD:
            self.dx = 0
            self.dy = 0
            self.action = 'dead'
            if self.dir == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.image = self.image
        else:
            self.pos_update()
            self.debuff_update()
            self.rect = self.rect.move(self.dx, self.dy) 

    def image_update(self):
        if self.index == self.len-2 and self.state == State.ATTACKING:
            self.state = State.ALIVE
        elif self.index == self.len - 2 and self.state == State.DEAD:
            self.completelydead = True
        self.index = (self.index + 0.5) % (self.len - 1)
        self.image = self.images[math.floor(self.index)]
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        
    def pos_update(self):

        self.dis = math.hypot(self.attack_pos[0] - self.rect.centerx, self.attack_pos[1] - self.rect.centery)
        if not Debuff.DIZZY in self.debuff and self.state != State.ATTACKING:
            if self.dis == 0:
                self.dx, self.dy = 0, 0
            else:
                self.dx, self.dy = ((self.attack_pos[0] - self.rect.centerx) / self.dis * self.speed, 
                                    (self.attack_pos[1] - self.rect.centery) / self.dis * self.speed)
            self.action = 'run'
            if (self.dis <= 10):
                self.state = State.ATTACKING
                self.dx = 0
                self.dy = 0
                self.action = 'attack'

        if not Debuff.DIZZY in self.debuff:
            if self.player.rect.centerx < self.rect.centerx: 
                self.dir = -1
                self.attack_pos = (self.player.rect.topright[0] + 80, self.player.rect.topright[1] - 80)
            elif self.player.rect.centerx > self.rect.centerx:
                self.dir = 1
                self.attack_pos = (self.player.rect.topleft[0] - 80, self.player.rect.topleft[1] - 80)

    def debuff_update(self):
         
        if Debuff.REPELL in self.debuff:
            self.dx = -self.dir * 30
            self.clicktock(3)
            if not self.isclocking:
                self.debuff.remove(Debuff.REPELL)
        elif Debuff.DIZZY in self.debuff:
            self.action = 'idle'
            self.dx = 0
            self.dy = 0
            self.clicktock(30)
            if not self.isclocking:
                self.debuff.remove(Debuff.DIZZY)

    def state_update(self):
        
        if self.hp <= 0:
            self.state = State.DEAD
        else:
            if self.check and not self.player.weapon.startattack and not self.player.weapon.cooling:
                self.check = False
                self.beingattacked = False

            if self.beingattacked and not self.check:
                self.check = True
                self.hp -= max(self.player.weapon.ATK - self.defence, 0)
                if self.player.weapon.skill == 'stab':
                    self.debuff.append(Debuff.REPELL)
                    self.action = 'hit'
                elif self.player.weapon.skill == 'spin':
                    self.debuff.append(Debuff.DIZZY)
                else:
                    self.action = 'hit'

    def draw(self):
        self.window.blit(self.image, self.rect)
        
        if self.state != State.DEAD:
            pygame.draw.rect(self.window, (255, 0, 0), [WindowSettings.width // 2 - 250, WindowSettings.height - 30, self.hp, 20], 0)
            self.window.blit(self.namerender, (WindowSettings.width // 2 - len(self.name) * 2 , WindowSettings.height - 40))