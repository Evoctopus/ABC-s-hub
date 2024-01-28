import pygame
import math

from Settings import *
from Attributes import *
from Weapon import *
from Monster import *


class Demon(Elite):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths, index_msg):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths, index_msg)
        
        self.rect.topleft = (x, y)
        self.tag = 'boss'
        self.set_attr(6000, 0.2, 10, 700, 0.5, 40)
        self.attack_pos = self.get_attack_pos()
        self.hp_coord = WindowSettings.width / self.hp 
        self.attackingindex = [7, 13]
        self.state = State.TALKING
        self.magic = 4
        self.attacking_method = AttackMethod.FIST
        self.attackrange = MonsterSettings.AttackingRange
        self.check = False
        self.proportion = 2
        self.recovering = False
        self.cooling = False
        self.dis = 0
        self.namefont = pygame.font.Font(None, NPCSettings.Fontsize*3)
        self.namerender = self.namefont.render('LUCIFER NIGHTFALL', True, NPCSettings.namecolor)
    

    def get_attack_pos(self):
        if self.state == State.SPELL or self.state == State.SUMMON:
            return self.rect.center
        return self.rect.midbottom

    def attacking_music(self):
        self.bgm.addsound('hit')

    def breathimage(self):
        return [pygame.transform.scale(pygame.image.load(f'assets/npc/demon/breath/{index}.png'), self.size) for index in range(1, 15)]
            
    def extra_state_update(self):

        if self.state == State.COOLING or self.state == State.ALIVE:
            if self.hp <= self.magic * 1200:
                self.magic -= 1
                self.ChangeActionTo(State.SPELL)
            else:
                if self.state == State.COOLING:
                    if self.is_cool_over():
                        self.ChangeActionTo(State.ALIVE)
                elif self.state == State.ALIVE and self.can_attack():
                    self.ChangeActionTo(State.ATTACKING)
        elif self.state == State.SPELL and self.dis == 0:
            self.ChangeActionTo(State.SUMMON)
    
    def extra_state_change(self, state):
        
        if state == State.SPELL:
            self.images = self.moveimage()
            self.speed = 6
            self.defence = 0.001
            self.spell(self.magic)
        elif state == State.SUMMON:
            self.images = self.breathimage()
            self.dir *= -1
            if self.magic == 3:
                self.bgm.addsound('summon')
            elif self.magic == 2:
                self.bgm.addsound('magic')
            elif self.magic == 1:
                self.bgm.addsound('cure') 
    
    def spell(self, magic):

        if magic == 3:
            self.location = (140, 60)
            self.path = r'assets\specialeffect\array\summon.png'
            self.center = (140, 140)
        if magic == 2:
            self.location = (1140, 60)
            self.path = r'assets\specialeffect\array\building.png'
            self.center = (1140, 140)
        if magic == 1:
            self.location = (140, 500)
            self.path = r'assets\specialeffect\array\recover.png'
            self.center = (140, 580)
        if magic == 0:
            self.location = (1140, 500)
            self.path = r'assets\specialeffect\array\curse.png'
            self.center = (1140, 580)
        self.array = pygame.transform.scale(pygame.image.load(self.path), (200, 200))
        self.array_rect = self.array.get_rect()
        self.array_rect.center = self.center
        self.angle = 0

    def recover(self):
        self.hp += 50
        self.recover_effect = TextSettings.Font1.render('+ 5 0', False, Color.Yellow)
        self.recovering = True
        self.recover_index = 0

    def draw(self):
        
        if self.state == State.SUMMON:
            self.angle += 2
            self.array = pygame.transform.scale(pygame.image.load(self.path), (200, 200))
            self.array = pygame.transform.rotate(self.array, self.angle)
            self.array_rect = self.array.get_rect()
            self.array_rect.center = self.center
            self.window.blit(self.array, self.array_rect)

        self.window.blit(self.image, self.rect) 
        if self.recovering:
            self.recover_effect.set_alpha(255 - self.recover_index*5)
            self.window.blit(self.recover_effect, (self.rect.centerx-self.recover_effect.get_width()/2, self.rect.centery - self.recover_index*0.5))
            self.recover_index += 1
        
        if self.state != State.DEAD:
            self.draw_effect(0, 50)
       