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
        self.before_rect = (x, y)

    def draw(self, window, dx=0, dy=0):
        pass

def gen_city_map():

    image_1 = [pygame.image.load(tile) for tile in GamePath.groundTiles]
    image_1 = [pygame.transform.scale(image,(SceneSettings.tileWidth,SceneSettings.tileHeight)) for image in image_1]
    
    image_2 = [pygame.image.load(tile) for tile in GamePath.roadTiles]
    image_2 = [pygame.transform.scale(image,(SceneSettings.tileWidth,
                                             SceneSettings.tileHeight)) for image in image_2]
    mapObj = []
    for i in range(SceneSettings.tileXnum):
        tmp_up = []
        for j in range(SceneSettings.tileYnum):
            if (i<=SceneSettings.tileXnum//2+3 and i >= SceneSettings.tileXnum//2-2) or (j <=SceneSettings.tileYnum//2+3 and j >= SceneSettings.tileYnum//2-2):
                tmp_up.append(image_2[randint(0, len(image_2) - 1)])
            else:
                tmp_up.append(image_1[randint(0, len(image_1) - 1)])
        mapObj.append(tmp_up)

    return mapObj

def gen_city_obstacle():
        
        image = [pygame.image.load(images) for images in GamePath.house]
        tree_image = [pygame.image.load(images) for images in GamePath.tree]
        block = pygame.sprite.Group()

        block.add(Block(image[1],150,30,160,200))
        block.add(Block(image[2], 440,50,90,90))
        block.add(Block(image[3],540,50,90,90))
        block.add(Block(image[4],150,675, 160, 160))
        block.add(Block(image[4],150,920, 160, 160))
        block.add(Block(image[5],600,675, 160, 160))
        block.add(Block(image[5],600,920, 160, 160))
        block.add(Block(image[6],1700,675, 160, 160))
        block.add(Block(image[7],1300,675, 160, 160))
        block.add(Block(image[8],1700,920, 160, 160))
        block.add(Block(image[9],1300,920, 160, 160))
        block.add(Block(image[10],375,675, 160, 160))
        block.add(Block(image[4],375,920, 160, 160))

        block.add(Block(tree_image[1],820,690,50,90))
        block.add(Block(tree_image[1],820,780,50,90))
        block.add(Block(tree_image[1],820,870,50,90))
        block.add(Block(tree_image[1],820,960,50,90))

        block.add(Block(tree_image[1],1130,690,50,90))
        block.add(Block(tree_image[1],1130,780,50,90))
        block.add(Block(tree_image[1],1130,870,50,90))
        block.add(Block(tree_image[1],1130,960,50,90))

        block.add(Block(tree_image[1],1130,20,50,90))
        block.add(Block(tree_image[1],1130,110,50,90))
        block.add(Block(tree_image[1],1130,200,50,90))
        block.add(Block(tree_image[1],1130,290,50,90))

        block.add(Block(tree_image[1],820,20,50,90))
        block.add(Block(tree_image[1],820,110,50,90))
        block.add(Block(tree_image[1],820,200,50,90))
        block.add(Block(tree_image[1],820,290,50,90))
    
        block.add(Block(tree_image[2],1800,250,100,150))
        block.add(Block(tree_image[2],1800,70,100,150))        
        block.add(Block(tree_image[3],1300,10,100,150))
        block.add(Block(tree_image[3],1470,250,100,150))
        block.add(Block(tree_image[3],1300,250,100,150))

        return block

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
    image = pygame.image.load(GamePath.tree[0]) 
    temp = pygame.image.load(GamePath.wildOBS[0])

    obstacles = pygame.sprite.Group()
    rightx = SceneSettings.tileXnum
    righty = SceneSettings.tileYnum//2
    for i in range(SceneSettings.tileXnum):
        for j in range(SceneSettings.tileYnum):
            # 防止在出生点生成obstacle
            if random() < SceneSettings.obstacleDensity and (not i in range(rightx-10, rightx+10)) and (not j in range(righty-10, righty+10)):
                if randint(1, 3) == 1:
                    if j <  SceneSettings.tileYnum//3 and i <= SceneSettings.tileXnum // 3:
                        obstacles.add(Block(temp, SceneSettings.tileWidth * i - 50, SceneSettings.tileHeight * j, 160, 160))
                else:
                    obstacles.add(Block(image, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))

    return obstacles    

def gen_ice_map():
    images = [pygame.image.load(tile) for tile in GamePath.iceTiles]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            tmp.append(images[randint(0, len(images) - 1)])
        mapObj.append(tmp)
    
    return mapObj
    
def gen_ice_obstacle():
    image = [pygame.image.load(obs) for obs in GamePath.iceOBS]

    obstacles = pygame.sprite.Group()

    midx = SceneSettings.tileXnum//2
    midy = SceneSettings.tileYnum//2
    for i in range(SceneSettings.tileXnum):
        for j in range(SceneSettings.tileYnum):
            # 防止在出生点生成obstacle
            if random() < SceneSettings.obstacleDensity and not(i < midx and j < midy) and (i not in range(midx-3, midx+3)) and (j not in range(midy-3, midy+3)):
                obstacles.add(Block(image[1], SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    
    return obstacles

def gen_lava_map():
    images = [pygame.image.load(tile) for tile in GamePath.lavaTiles]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            tmp.append(images[randint(0, len(images) - 1)])
        mapObj.append(tmp)
    
    return mapObj

def gen_lava_obstacle():
    image = [pygame.image.load(obs) for obs in GamePath.lavaOBS]
    
    obstacles = pygame.sprite.Group()

    midx = SceneSettings.tileXnum//2
    midy = SceneSettings.tileYnum//2
    for i in range(SceneSettings.tileXnum):
        for j in range(SceneSettings.tileYnum):
            # 防止在出生点生成obstacle
            if random() < SceneSettings.obstacleDensity and not(i < midx and j < midy) and (i not in range(midx-3, midx+3)) and (j not in range(midy-3, midy+3)):
                obstacles.add(Block(image[1], SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    obstacles.add(Block(image[2],WindowSettings.width//2-175, WindowSettings.height//2-175,50,100))
    obstacles.add(Block(image[2],WindowSettings.width//2+110, WindowSettings.height//2-175,50,100))
    obstacles.add(Block(image[2],WindowSettings.width//2-175, WindowSettings.height//2+115,50,100))
    obstacles.add(Block(image[2],WindowSettings.width//2+110, WindowSettings.height//2+115,50,100))        

    return obstacles

def gen_boss_map():

    images = [pygame.transform.scale(pygame.image.load(f'./assets/tiles/boss{i}.png'), (SceneSettings.tileWidth, SceneSettings.tileHeight)) for i in range(1, 7)]

    mapObj = []
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            tmp.append(images[randint(0, len(images) - 1)])
        mapObj.append(tmp)
    
    return mapObj

def gen_boss_obstacle():

    image = pygame.image.load(GamePath.bossWall) 
    obstacles = pygame.sprite.Group()
    for i in range(SceneSettings.tileXnum_small):
        for j in range(SceneSettings.tileYnum_small):
            if (((i==0 or i==SceneSettings.tileXnum_small-1 or i == 6 or i == SceneSettings.tileXnum_small-7) and (j<=6 or j>=SceneSettings.tileYnum_small-7)) or 
                ((j==0 or j==6 or j==SceneSettings.tileYnum_small-7 or j==SceneSettings.tileYnum_small-1) and (i<=6 or i>=SceneSettings.tileXnum_small-7))):
                obstacles.add(Block(image, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    return obstacles  

class Cherry_blossom_tree(pygame.sprite.Sprite):

    def __init__(self, window, x=1550, y=100):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load(image),(250,300)) for image in GamePath.cherry_blossom_tree]
        self.rect = self.images[0].get_rect()
        self.rect.topleft = (x, y)
        self.before_rect = (x,y)
        self.index = 0
        self.window = window
        
    def update(self):
        self.index = (self.index + 1) % len(self.images)
        self.image = self.images[self.index]
        self.window.blit(self.image,self.rect)