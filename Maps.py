# -*- coding:utf-8 -*-

import pygame

from Settings import *
from random import random, randint

class Block(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0, width=SceneSettings.tileWidth, height=SceneSettings.tileHeight):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


    def draw(self, window, dx=0, dy=0):
        pass

def gen_wild_map():

    images = [pygame.image.load(tile) for tile in GamePath.groundTiles]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            tmp.append(images[randint(0, len(images) - 1)])
        mapObj.append(tmp)
    
    return mapObj

def gen_wild_obstacle():
    image = pygame.image.load(GamePath.tree) 

    obstacles = pygame.sprite.Group()
    # donot generate in the original position of player
    # 左上没生成障碍，因为没做npc和障碍的碰撞
    midx = SceneSettings.tileXnum//2
    midy = SceneSettings.tileYnum//2
    for i in range(SceneSettings.tileXnum):
        for j in range(SceneSettings.tileYnum):
            # 防止在出生点生成obstacle
            if random() < SceneSettings.obstacleDensity and not(i < midx and j < midy) and (i not in range(midx-3, midx+3)) and (j not in range(midy-3, midy+3)):
                obstacles.add(Block(image, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    return obstacles    

def gen_city_map():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####

def gen_boss_map():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####

def gen_city_obstacle():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####



def gen_boss_obstacle():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####
