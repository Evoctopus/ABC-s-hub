import pygame
from random import randint
import math

from Settings import *
from Attributes import *
from Weapon import *



class Coin(pygame.sprite.Sprite, Collidable):
    def __init__(self, window, player, cointype, angle, bgm, *rect) :
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self, window, bgm)
        self.images = [pygame.transform.scale(pygame.image.load(f"./assets/coin/{cointype}/{i}.png"), CoinSettings.size) 
                       for i in range(1, 5)]
        self.type = cointype
        self.value = CoinSettings.value[self.type]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = rect
        self.window = window
        self.index = 0
        self.angle = angle
        self.player = player
        self.speed = randint(20, 25)
        self.disappear = False
        self.hasspill = False
        self.spilltime = 15
        self.bgm = bgm

    
    def spillout(self):
        self.dx = math.sin(self.angle) * self.speed / (self.spilltime + 1 - self.click)
        self.dy = math.cos(self.angle) * self.speed / (self.spilltime + 1 - self.click)

    def track_player(self):
        self.dis = math.hypot(self.player.rect.centerx - self.rect.centerx, self.player.rect.centery - self.rect.centery)
        if self.dis <= 5:
            self.disappear = True
            self.bgm.addsound('coin')
            self.player.attr_update(addCoins = self.value)
        else:
            self.dx, self.dy = ((self.player.rect.centerx - self.rect.centerx) / self.dis * self.speed, 
                                (self.player.rect.centery - self.rect.centery) / self.dis * self.speed)
        
    
    def image_update(self):
        self.index = (self.index + 0.5) % 3
        self.image = self.images[math.floor(self.index)]
    
    def pos_update(self):
        
        if not self.hasspill:
            self.clicktock(self.spilltime)
            self.spillout()
            if not self.isclocking:
                self.hasspill = True
        else:
            self.track_player()
        self.rect = self.rect.move(self.dx, self.dy)

    def update(self):
        self.image_update()
        self.pos_update()
    
    def draw(self):
        self.window.blit(self.image, self.rect)
    

