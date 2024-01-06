# -*- coding:utf-8 -*-
import pygame

class Collidable:
    def __init__(self):
        self.collidingWith = {
            "obstacle": False, 
            "npc": False, 
            "monster": False, 
            "portal": False, 
            "boss": False, 
        }
        self.collidingObject = {
            "obstacle": pygame.sprite.Group(), 
            "npc": pygame.sprite.Group(),
            "monster": pygame.sprite.Group(), 
            "portal": pygame.sprite.Group(), 
            "boss": None, 
        }
        self.boss = None
        self.click = 0
        self.isclocking = False

    
    
    def is_colliding(self):
        return (self.collidingWith["obstacle"] or 
                self.collidingWith["npc"] or 
                self.collidingWith["monster"] or
                self.collidingWith["portal"] or 
                self.collidingWith["boss"])

    def clicktock(self, time):
        if not self.isclocking:
            self.isclocking = True
            self.click = time
        else:
            self.click -= 1
            if self.click == 1:
                self.isclocking = False    #计时器